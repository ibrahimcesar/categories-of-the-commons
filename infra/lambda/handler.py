"""
AWS Lambda handler for GitHub data collection.
Runs as part of the Categories of the Commons serverless infrastructure.

Supports chunked execution with self-invocation for large projects that
exceed the 15-minute Lambda timeout.
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

# Chunking configuration
COMMIT_BATCH_SIZE = 500  # Commits per chunk
PR_BATCH_SIZE = 100  # PRs per chunk
ISSUE_BATCH_SIZE = 100  # Issues per chunk
MIN_REMAINING_TIME_MS = 60000  # 60 seconds buffer before timeout
SELF_INVOKE_BUFFER_MS = 120000  # 2 minutes buffer to allow self-invoke

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


def get_remaining_time_ms(context) -> int:
    """Get remaining execution time in milliseconds."""
    if context and hasattr(context, 'get_remaining_time_in_millis'):
        return context.get_remaining_time_in_millis()
    return 900000  # Default 15 minutes if no context


def should_continue(context) -> bool:
    """Check if we have enough time to continue processing."""
    remaining = get_remaining_time_ms(context)
    return remaining > MIN_REMAINING_TIME_MS


def should_self_invoke(context) -> bool:
    """Check if we should self-invoke to continue."""
    remaining = get_remaining_time_ms(context)
    return remaining < SELF_INVOKE_BUFFER_MS


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

    def get_in_progress_projects(self) -> List[Dict[str, Any]]:
        """Get in-progress projects (may have checkpoints)."""
        response = self.table.query(
            IndexName="status-index",
            KeyConditionExpression="status = :status",
            ExpressionAttributeValues={":status": "in_progress"}
        )
        return response.get("Items", [])

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

    def save_checkpoint(self, repo: str, checkpoint: Dict[str, Any]) -> None:
        """Save checkpoint for partial collection."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET checkpoint = :checkpoint, updated_at = :now",
            ExpressionAttributeValues={
                ":checkpoint": checkpoint,
                ":now": now
            }
        )

    def get_checkpoint(self, repo: str) -> Optional[Dict[str, Any]]:
        """Get checkpoint for a project."""
        response = self.table.get_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"}
        )
        item = response.get("Item", {})
        return item.get("checkpoint")

    def clear_checkpoint(self, repo: str) -> None:
        """Clear checkpoint after completion."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="REMOVE checkpoint SET updated_at = :now",
            ExpressionAttributeValues={":now": now}
        )

    def save_partial_data(self, repo: str, partial_data: Dict[str, Any]) -> None:
        """Save partial collected data to continue later."""
        now = datetime.now(timezone.utc).isoformat()
        # Store as JSON string since DynamoDB has limits on nested objects
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET partial_data = :data, updated_at = :now",
            ExpressionAttributeValues={
                ":data": json.dumps(partial_data, default=str),
                ":now": now
            }
        )

    def get_partial_data(self, repo: str) -> Optional[Dict[str, Any]]:
        """Get partial collected data."""
        response = self.table.get_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"}
        )
        item = response.get("Item", {})
        partial_json = item.get("partial_data")
        if partial_json:
            return json.loads(partial_json)
        return None

    def mark_completed(self, repo: str, s3_key: str) -> None:
        """Mark project as completed."""
        now = datetime.now(timezone.utc).isoformat()
        self.table.update_item(
            Key={"pk": f"PROJECT#{repo}", "sk": "STATUS"},
            UpdateExpression="SET #status = :status, updated_at = :now, s3_key = :key, completed_at = :now REMOVE checkpoint, partial_data",
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
            UpdateExpression="SET #status = :status, updated_at = :now, error = :error REMOVE checkpoint, partial_data",
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
# Chunked Data Collection
# =============================================================================

class ChunkedGitHubCollector:
    """GitHub collector with chunked execution support."""

    # Collection phases
    PHASE_REPO = "repo"
    PHASE_CONTRIBUTORS = "contributors"
    PHASE_GOVERNANCE = "governance"
    PHASE_COMMITS = "commits"
    PHASE_PRS = "prs"
    PHASE_ISSUES = "issues"
    PHASE_COMPLETE = "complete"

    PHASES_ORDER = [PHASE_REPO, PHASE_CONTRIBUTORS, PHASE_GOVERNANCE,
                    PHASE_COMMITS, PHASE_PRS, PHASE_ISSUES, PHASE_COMPLETE]

    def __init__(self, token: str, context=None):
        self.token = token
        auth = Auth.Token(token)
        self.github = Github(auth=auth)
        self.context = context

    def collect_project_chunked(
        self,
        repo_full_name: str,
        since_days: int = 365,
        checkpoint: Optional[Dict[str, Any]] = None,
        partial_data: Optional[Dict[str, Any]] = None
    ) -> tuple[Dict[str, Any], Optional[Dict[str, Any]], bool]:
        """
        Collect data for a project with chunking support.

        Returns:
            tuple: (data, new_checkpoint, is_complete)
            - data: Collected data so far
            - new_checkpoint: Checkpoint to continue from (None if complete)
            - is_complete: True if collection is finished
        """
        print(f"Collecting: {repo_full_name}")

        # Initialize or restore data
        if partial_data:
            data = partial_data
            print(f"  Resuming from partial data, phase: {checkpoint.get('phase', 'unknown')}")
        else:
            data = {
                "metadata": {
                    "repo": repo_full_name,
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                    "collection_period_days": since_days,
                    "source": "lambda_chunked"
                }
            }

        # Determine starting phase
        if checkpoint:
            current_phase = checkpoint.get("phase", self.PHASE_REPO)
            phase_offset = checkpoint.get("offset", 0)
        else:
            current_phase = self.PHASE_REPO
            phase_offset = 0

        try:
            repo = self.github.get_repo(repo_full_name)
            since_date = datetime.now(timezone.utc) - timedelta(days=since_days)

            # Process phases in order
            phase_idx = self.PHASES_ORDER.index(current_phase)

            for phase in self.PHASES_ORDER[phase_idx:]:
                # Check if we should continue
                if not should_continue(self.context):
                    print(f"  ⏱️ Running low on time, checkpointing at phase: {phase}")
                    new_checkpoint = {"phase": phase, "offset": phase_offset}
                    return data, new_checkpoint, False

                print(f"  Phase: {phase}")

                if phase == self.PHASE_REPO:
                    data["repository"] = self._collect_repo_metrics(repo)
                    phase_offset = 0

                elif phase == self.PHASE_CONTRIBUTORS:
                    data["contributors"] = self._collect_contributors(repo)
                    phase_offset = 0

                elif phase == self.PHASE_GOVERNANCE:
                    data["governance_files"] = self._check_governance_files(repo)
                    phase_offset = 0

                elif phase == self.PHASE_COMMITS:
                    result = self._collect_commits_chunked(
                        repo, since_date, phase_offset
                    )

                    if "recent_commits" not in data:
                        data["recent_commits"] = []
                    data["recent_commits"].extend(result["commits"])

                    if not result["complete"]:
                        new_checkpoint = {
                            "phase": self.PHASE_COMMITS,
                            "offset": result["next_offset"]
                        }
                        print(f"  ⏱️ Commits incomplete, collected {len(data['recent_commits'])} so far")
                        return data, new_checkpoint, False

                    print(f"  ✓ Collected {len(data['recent_commits'])} commits total")
                    phase_offset = 0

                elif phase == self.PHASE_PRS:
                    data["pull_requests"] = self._collect_pr_stats(repo, since_date)
                    phase_offset = 0

                elif phase == self.PHASE_ISSUES:
                    data["issues"] = self._collect_issue_stats(repo, since_date)
                    phase_offset = 0

                elif phase == self.PHASE_COMPLETE:
                    data["metadata"]["completed_at"] = datetime.now(timezone.utc).isoformat()
                    return data, None, True

            return data, None, True

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

    def _collect_commits_chunked(
        self,
        repo,
        since_date: datetime,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Collect commits in chunks with time-awareness.

        Returns dict with:
        - commits: List of collected commits
        - complete: Whether all commits were collected
        - next_offset: Offset to continue from if incomplete
        """
        commits = []
        current_offset = 0
        collected_in_batch = 0

        try:
            commits_iter = repo.get_commits(since=since_date)

            for commit in commits_iter:
                # Skip to offset if resuming
                if current_offset < offset:
                    current_offset += 1
                    continue

                # Check time periodically
                if collected_in_batch > 0 and collected_in_batch % 50 == 0:
                    if not should_continue(self.context):
                        return {
                            "commits": commits,
                            "complete": False,
                            "next_offset": current_offset
                        }

                # Check batch size
                if collected_in_batch >= COMMIT_BATCH_SIZE:
                    return {
                        "commits": commits,
                        "complete": False,
                        "next_offset": current_offset
                    }

                commits.append({
                    "sha": commit.sha,
                    "author": commit.commit.author.name if commit.commit.author else None,
                    "author_login": commit.author.login if commit.author else None,
                    "date": commit.commit.author.date.isoformat() if commit.commit.author else None,
                    "message": commit.commit.message[:200] if commit.commit.message else None,
                })

                current_offset += 1
                collected_in_batch += 1

        except Exception as e:
            print(f"Error collecting commits: {e}")

        return {
            "commits": commits,
            "complete": True,
            "next_offset": current_offset
        }

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
                if i >= PR_BATCH_SIZE:
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
                if i >= ISSUE_BATCH_SIZE:
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
# Self-Invocation
# =============================================================================

def invoke_continuation(function_name: str, event: Dict[str, Any]) -> None:
    """Invoke Lambda to continue processing."""
    print(f"🔄 Self-invoking to continue: {event.get('continue_repo', 'batch')}")

    lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='Event',  # Async invocation
        Payload=json.dumps(event)
    )


# =============================================================================
# Lambda Handler
# =============================================================================

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Main Lambda handler with chunked execution support.

    Event can include:
    - action: "collect" (default), "init", "status", "retry"
    - projects: List of projects for init action
    - category: Category for init action
    - continue_repo: Repo to continue collecting (for self-invocation)
    """
    print(f"Event: {json.dumps(event)}")

    # Get function name for self-invocation
    function_name = os.environ.get("AWS_LAMBDA_FUNCTION_NAME", "github-collector")

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

        collector = ChunkedGitHubCollector(token, context)
        collected = 0
        failed = 0
        continued = 0

        # Check for continuation of specific repo
        continue_repo = event.get("continue_repo")

        if continue_repo:
            # Continue collecting a specific repo
            print(f"📍 Continuing collection for: {continue_repo}")
            checkpoint = state_manager.get_checkpoint(continue_repo)
            partial_data = state_manager.get_partial_data(continue_repo)

            try:
                data, new_checkpoint, is_complete = collector.collect_project_chunked(
                    continue_repo,
                    since_days=COLLECTION_DAYS,
                    checkpoint=checkpoint,
                    partial_data=partial_data
                )

                if is_complete:
                    # Save to S3
                    s3_key = f"raw/{continue_repo.replace('/', '_')}_data.json"
                    s3.put_object(
                        Bucket=BUCKET_NAME,
                        Key=s3_key,
                        Body=json.dumps(data, indent=2, default=str),
                        ContentType="application/json"
                    )
                    state_manager.mark_completed(continue_repo, s3_key)
                    collected += 1
                    print(f"✅ Completed: {continue_repo}")
                else:
                    # Save checkpoint and partial data, then self-invoke
                    state_manager.save_checkpoint(continue_repo, new_checkpoint)
                    state_manager.save_partial_data(continue_repo, data)

                    # Self-invoke to continue
                    invoke_continuation(function_name, {
                        "action": "collect",
                        "continue_repo": continue_repo
                    })
                    continued += 1
                    print(f"⏸️ Checkpointed: {continue_repo}, self-invoking to continue")

            except Exception as e:
                error_msg = str(e)
                state_manager.mark_failed(continue_repo, error_msg)
                failed += 1
                print(f"❌ Failed: {continue_repo} - {error_msg}")

        else:
            # First check for in-progress projects (may have checkpoints from previous run)
            in_progress = state_manager.get_in_progress_projects()

            for project_item in in_progress:
                repo = project_item["repo"]
                print(f"📍 Resuming in-progress: {repo}")
                checkpoint = state_manager.get_checkpoint(repo)
                partial_data = state_manager.get_partial_data(repo)

                # Check rate limit
                rate_info = get_rate_limit(token)
                if rate_info["remaining"] < MIN_RATE_LIMIT:
                    print("Rate limit low. Stopping collection.")
                    break

                try:
                    data, new_checkpoint, is_complete = collector.collect_project_chunked(
                        repo,
                        since_days=COLLECTION_DAYS,
                        checkpoint=checkpoint,
                        partial_data=partial_data
                    )

                    if is_complete:
                        s3_key = f"raw/{repo.replace('/', '_')}_data.json"
                        s3.put_object(
                            Bucket=BUCKET_NAME,
                            Key=s3_key,
                            Body=json.dumps(data, indent=2, default=str),
                            ContentType="application/json"
                        )
                        state_manager.mark_completed(repo, s3_key)
                        collected += 1
                        print(f"✅ Completed: {repo}")
                    else:
                        state_manager.save_checkpoint(repo, new_checkpoint)
                        state_manager.save_partial_data(repo, data)
                        invoke_continuation(function_name, {
                            "action": "collect",
                            "continue_repo": repo
                        })
                        continued += 1
                        print(f"⏸️ Checkpointed: {repo}")

                except Exception as e:
                    error_msg = str(e)
                    state_manager.mark_failed(repo, error_msg)
                    failed += 1
                    print(f"❌ Failed: {repo} - {error_msg}")

            # Get pending projects if we have time
            if should_continue(context):
                pending = state_manager.get_pending_projects(limit=PROJECTS_PER_RUN)

                for repo in pending:
                    # Check rate limit before each project
                    rate_info = get_rate_limit(token)
                    if rate_info["remaining"] < MIN_RATE_LIMIT:
                        print("Rate limit low. Stopping collection.")
                        break

                    # Check time
                    if not should_continue(context):
                        print("Running low on time. Stopping collection.")
                        break

                    state_manager.mark_in_progress(repo)

                    try:
                        data, new_checkpoint, is_complete = collector.collect_project_chunked(
                            repo,
                            since_days=COLLECTION_DAYS
                        )

                        if is_complete:
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
                        else:
                            # Save checkpoint and self-invoke
                            state_manager.save_checkpoint(repo, new_checkpoint)
                            state_manager.save_partial_data(repo, data)

                            invoke_continuation(function_name, {
                                "action": "collect",
                                "continue_repo": repo
                            })
                            continued += 1
                            print(f"⏸️ Checkpointed: {repo}, self-invoking to continue")

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
            "continued": continued,
            "remaining_in_queue": stats["pending"],
            "in_progress": stats["in_progress"],
            "rate_limit_remaining": get_rate_limit(token)["remaining"]
        }

    else:
        return {"status": "error", "message": f"Unknown action: {action}"}
