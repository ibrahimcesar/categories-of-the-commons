"""
AWS Lambda handler for GitHub data collection.
Runs as part of the Categories of the Commons serverless infrastructure.
"""

import os
import json
import time
import boto3
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests
from github import Github, Auth


# =============================================================================
# Configuration
# =============================================================================

BUCKET_NAME = os.environ.get("BUCKET_NAME")
TABLE_NAME = os.environ.get("TABLE_NAME")
TOKEN_PARAMETER_NAME = os.environ.get("TOKEN_PARAMETER_NAME", "/github-collector/token")
PROJECTS_PER_RUN = int(os.environ.get("PROJECTS_PER_RUN", "5"))
COLLECTION_DAYS = int(os.environ.get("COLLECTION_DAYS", "365"))
MIN_RATE_LIMIT = 500  # Stop when rate limit falls below this

# AWS clients
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
ssm = boto3.client("ssm")
lambda_client = boto3.client("lambda")


def get_github_token() -> str:
    """Retrieve GitHub token from SSM Parameter Store."""
    response = ssm.get_parameter(
        Name=TOKEN_PARAMETER_NAME,
        WithDecryption=True
    )
    return response["Parameter"]["Value"]


def get_rate_limit(token: str) -> Dict[str, Any]:
    """Check GitHub API rate limit."""
    response = requests.get(
        "https://api.github.com/rate_limit",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        },
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        core = data["resources"]["core"]
        return {
            "remaining": core["remaining"],
            "limit": core["limit"],
            "reset": datetime.fromtimestamp(core["reset"], tz=timezone.utc).isoformat()
        }
    return {"remaining": 0, "limit": 5000, "reset": None}


# =============================================================================
# State Management (DynamoDB)
# =============================================================================

class DynamoDBStateManager:
    """Manages collection state in DynamoDB."""

    def __init__(self, table_name: str):
        self.table = dynamodb.Table(table_name)

    def initialize_queue(self, projects: List[str], category: str) -> int:
        """Initialize queue with projects."""
        added = 0
        now = datetime.now(timezone.utc).isoformat()

        with self.table.batch_writer() as batch:
            for project in projects:
                batch.put_item(Item={
                    "pk": f"PROJECT#{project}",
                    "sk": "STATUS",
                    "repo": project,
                    "category": category,
                    "status": "pending",
                    "created_at": now,
                    "updated_at": now
                })
                added += 1

        return added

    def get_pending_projects(self, limit: int = 10) -> List[str]:
        """Get pending projects from queue."""
        response = self.table.query(
            IndexName="status-index",
            KeyConditionExpression="status = :status",
            ExpressionAttributeValues={":status": "pending"},
            Limit=limit
        )
        return [item["repo"] for item in response.get("Items", [])]

    def mark_in_progress(self, repo: str) -> None:
        """Mark project as in progress."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET #status = :status, updated_at = :now",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "in_progress",
                ":now": now
            }
        )

    def mark_completed(self, repo: str, s3_key: str) -> None:
        """Mark project as completed."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET #status = :status, updated_at = :now, s3_key = :key, completed_at = :now",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "completed",
                ":now": now,
                ":key": s3_key
            }
        )

    def mark_failed(self, repo: str, error: str) -> None:
        """Mark project as failed."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET #status = :status, updated_at = :now, error = :error",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "failed",
                ":now": now,
                ":error": error
            }
        )

    def get_stats(self) -> Dict[str, int]:
        """Get collection statistics."""
        stats = {"pending": 0, "in_progress": 0, "completed": 0, "failed": 0}

        for status in stats.keys():
            response = self.table.query(
                IndexName="status-index",
                KeyConditionExpression="status = :status",
                ExpressionAttributeValues={":status": status},
                Select="COUNT"
            )
            stats[status] = response.get("Count", 0)

        return stats


# =============================================================================
# Data Collection (Simplified for Lambda)
# =============================================================================

class LambdaGitHubCollector:
    """Simplified GitHub collector for Lambda execution."""

    def __init__(self, token: str):
        self.token = token
        auth = Auth.Token(token)
        self.github = Github(auth=auth)

    def collect_project(self, repo_full_name: str, since_days: int = 365) -> Dict[str, Any]:
        """Collect data for a single project."""
        print(f"Collecting: {repo_full_name}")

        try:
            repo = self.github.get_repo(repo_full_name)
            since_date = datetime.now(timezone.utc) - timedelta(days=since_days)

            data = {
                "metadata": {
                    "repo": repo_full_name,
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "collection_period_days": since_days,
                    "source": "lambda"
                },
                "repository": self._collect_repo_metrics(repo),
                "contributors": self._collect_contributors(repo),
                "governance_files": self._check_governance_files(repo),
                "pull_requests": self._collect_pr_stats(repo, since_date),
                "issues": self._collect_issue_stats(repo, since_date),
            }

            return data

        except Exception as e:
            print(f"Error collecting {repo_full_name}: {e}")
            raise

    def _collect_repo_metrics(self, repo) -> Dict[str, Any]:
        """Collect basic repository metrics."""
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "stargazers_count": repo.stargazers_count,
            "forks_count": repo.forks_count,
            "open_issues_count": repo.open_issues_count,
            "language": repo.language,
            "topics": repo.get_topics(),
            "license": repo.license.name if repo.license else None,
            "has_wiki": repo.has_wiki,
            "has_discussions": repo.has_discussions,
            "archived": repo.archived,
            "default_branch": repo.default_branch,
        }

    def _collect_contributors(self, repo, max_count: int = 100) -> List[Dict[str, Any]]:
        """Collect contributor data."""
        contributors = []
        try:
            for i, contributor in enumerate(repo.get_contributors()):
                if i >= max_count:
                    break
                contributors.append({
                    "login": contributor.login,
                    "contributions": contributor.contributions,
                    "type": contributor.type
                })
        except Exception as e:
            print(f"Error collecting contributors: {e}")
        return contributors

    def _check_governance_files(self, repo) -> Dict[str, bool]:
        """Check for governance-related files."""
        files = [
            "GOVERNANCE.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
            "SECURITY.md", "MAINTAINERS.md", ".github/CODEOWNERS"
        ]
        results = {}
        for file_path in files:
            try:
                repo.get_contents(file_path)
                results[file_path] = True
            except:
                results[file_path] = False
        return results

    def _collect_pr_stats(self, repo, since_date: datetime) -> Dict[str, Any]:
        """Collect PR statistics."""
        stats = {
            "total_merged": 0,
            "total_closed_unmerged": 0,
            "total_open": 0,
            "merge_times_hours": [],
        }

        try:
            # Sample of closed PRs
            for i, pr in enumerate(repo.get_pulls(state="closed", sort="updated", direction="desc")):
                if i >= 100:
                    break
                if pr.updated_at < since_date:
                    break

                if pr.merged:
                    stats["total_merged"] += 1
                    if pr.merged_at and pr.created_at:
                        merge_time = (pr.merged_at - pr.created_at).total_seconds() / 3600
                        stats["merge_times_hours"].append(merge_time)
                else:
                    stats["total_closed_unmerged"] += 1

            # Count open PRs
            stats["total_open"] = repo.get_pulls(state="open").totalCount

        except Exception as e:
            print(f"Error collecting PR stats: {e}")

        # Calculate average
        if stats["merge_times_hours"]:
            stats["avg_merge_time_hours"] = sum(stats["merge_times_hours"]) / len(stats["merge_times_hours"])
        else:
            stats["avg_merge_time_hours"] = 0

        return stats

    def _collect_issue_stats(self, repo, since_date: datetime) -> Dict[str, Any]:
        """Collect issue statistics."""
        stats = {
            "total_closed": 0,
            "total_open": 0,
            "close_times_hours": [],
            "labels": {}
        }

        try:
            # Sample of closed issues
            for i, issue in enumerate(repo.get_issues(state="closed", since=since_date)):
                if i >= 100:
                    break
                if issue.pull_request:
                    continue

                stats["total_closed"] += 1

                if issue.closed_at and issue.created_at:
                    close_time = (issue.closed_at - issue.created_at).total_seconds() / 3600
                    stats["close_times_hours"].append(close_time)

                for label in issue.labels:
                    label_name = label.name.lower()
                    stats["labels"][label_name] = stats["labels"].get(label_name, 0) + 1

            # Count open issues
            stats["total_open"] = repo.get_issues(state="open").totalCount

        except Exception as e:
            print(f"Error collecting issue stats: {e}")

        # Calculate average
        if stats["close_times_hours"]:
            stats["avg_close_time_hours"] = sum(stats["close_times_hours"]) / len(stats["close_times_hours"])
        else:
            stats["avg_close_time_hours"] = 0

        return stats


# =============================================================================
# Lambda Handler
# =============================================================================

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main Lambda handler.

    Event can include:
    - action: "collect" (default), "init", "status", "retry"
    - projects: List of projects for init action
    - category: Category for init action
    """
    print(f"Event: {json.dumps(event)}")

    action = event.get("action", "collect")
    state_manager = DynamoDBStateManager(TABLE_NAME)

    if action == "init":
        # Initialize queue with projects
        projects = event.get("projects", [])
        category = event.get("category", "unknown")
        added = state_manager.initialize_queue(projects, category)
        return {"status": "initialized", "projects_added": added}

    elif action == "status":
        # Return current stats
        stats = state_manager.get_stats()
        return {"status": "ok", "stats": stats}

    elif action == "retry":
        # Re-queue failed projects (would need additional implementation)
        return {"status": "not_implemented"}

    elif action == "collect":
        # Main collection logic
        token = get_github_token()
        rate_info = get_rate_limit(token)

        print(f"Rate limit: {rate_info['remaining']}/{rate_info.get('limit', 5000)}")

        if rate_info["remaining"] < MIN_RATE_LIMIT:
            print(f"Rate limit too low ({rate_info['remaining']}). Skipping this run.")
            return {
                "status": "rate_limited",
                "remaining": rate_info["remaining"],
                "reset": rate_info["reset"]
            }

        # Get pending projects
        pending = state_manager.get_pending_projects(limit=PROJECTS_PER_RUN)

        if not pending:
            print("No pending projects.")
            return {"status": "complete", "collected": 0}

        collector = LambdaGitHubCollector(token)
        collected = 0
        failed = 0

        for repo in pending:
            # Check rate limit before each project
            rate_info = get_rate_limit(token)
            if rate_info["remaining"] < MIN_RATE_LIMIT:
                print(f"Rate limit low. Stopping collection.")
                break

            state_manager.mark_in_progress(repo)

            try:
                data = collector.collect_project(repo, since_days=COLLECTION_DAYS)

                # Save to S3
                s3_key = f"raw/{repo.replace('/', '_')}_data.json"
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=s3_key,
                    Body=json.dumps(data, indent=2, default=str),
                    ContentType="application/json"
                )

                state_manager.mark_completed(repo, s3_key)
                collected += 1
                print(f"✅ Collected: {repo}")

            except Exception as e:
                error_msg = str(e)
                state_manager.mark_failed(repo, error_msg)
                failed += 1
                print(f"❌ Failed: {repo} - {error_msg}")

        # Get updated stats
        stats = state_manager.get_stats()

        return {
            "status": "ok",
            "collected": collected,
            "failed": failed,
            "remaining_in_queue": stats["pending"],
            "rate_limit_remaining": get_rate_limit(token)["remaining"]
        }

    else:
        return {"status": "error", "message": f"Unknown action: {action}"}
