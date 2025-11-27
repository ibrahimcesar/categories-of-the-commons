"""
GitHub Data Collector
Collects repository metrics, commits, PRs, issues, and contributor data from GitHub API.
"""

import os
import time
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path

import requests
import warnings
from github import Github, RateLimitExceededException, Auth
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Suppress OpenSSL warning
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL")


class GitHubCollector:
    """Collects data from GitHub repositories."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub collector.

        Args:
            token: GitHub personal access token. If None, reads from GITHUB_TOKEN env var.
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN env var or pass token parameter.")

        # Use newer PyGithub Auth API
        auth = Auth.Token(self.token)
        self.github = Github(auth=auth)

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        })

    def get_rate_limit(self) -> Dict[str, Any]:
        """Get current GitHub API rate limit status."""
        rate_limit = self.github.get_rate_limit()

        # Handle different PyGithub API versions
        # Newer versions use rate.core, older use core directly
        if hasattr(rate_limit, 'core'):
            core = rate_limit.core
            search = rate_limit.search
        else:
            # Fallback for newer API structure
            core = rate_limit.rate
            search = rate_limit.rate

        return {
            "core": {
                "remaining": core.remaining,
                "limit": core.limit,
                "reset": core.reset
            },
            "search": {
                "remaining": search.remaining if hasattr(rate_limit, 'search') else core.remaining,
                "limit": search.limit if hasattr(rate_limit, 'search') else core.limit,
                "reset": search.reset if hasattr(rate_limit, 'search') else core.reset
            }
        }

    def collect_repository_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """
        Collect basic repository metrics.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            Dictionary containing repository metrics
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
                "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
                "size": repo.size,
                "stargazers_count": repo.stargazers_count,
                "watchers_count": repo.watchers_count,
                "forks_count": repo.forks_count,
                "open_issues_count": repo.get_issues(state='open').totalCount,
                "language": repo.language,
                "topics": repo.get_topics(),
                "has_wiki": repo.has_wiki,
                "has_pages": repo.has_pages,
                "has_discussions": repo.has_discussions,
                "archived": repo.archived,
                "disabled": repo.disabled,
                "default_branch": repo.default_branch,
                "license": repo.license.name if repo.license else None,
                "collected_at": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            print(f"Error collecting metrics for {repo_full_name}: {e}")
            return {"error": str(e), "repo": repo_full_name}

    def collect_contributor_data(self, repo_full_name: str, max_contributors: int = 100) -> List[Dict[str, Any]]:
        """
        Collect contributor data for entropy calculation.

        Args:
            repo_full_name: Repository in format "owner/repo"
            max_contributors: Maximum number of contributors to fetch

        Returns:
            List of contributor dictionaries
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            contributors = []

            for contributor in tqdm(repo.get_contributors()[:max_contributors], desc="Contributors"):
                contributors.append({
                    "login": contributor.login,
                    "contributions": contributor.contributions,
                    "type": contributor.type
                })

            return contributors
        except Exception as e:
            print(f"Error collecting contributors for {repo_full_name}: {e}")
            return []

    def collect_commit_history(self, repo_full_name: str, since_days: int = 365) -> List[Dict[str, Any]]:
        """
        Collect recent commit history for temporal analysis.

        Args:
            repo_full_name: Repository in format "owner/repo"
            since_days: Number of days of history to collect

        Returns:
            List of commit dictionaries
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            since_date = datetime.now(timezone.utc) - timedelta(days=since_days)
            commits = []

            for commit in tqdm(repo.get_commits(since=since_date), desc="Commits"):
                commits.append({
                    "sha": commit.sha,
                    "author": commit.commit.author.name,
                    "author_login": commit.author.login if commit.author else None,
                    "date": commit.commit.author.date.isoformat(),
                    "message": commit.commit.message,
                    "additions": commit.stats.additions,
                    "deletions": commit.stats.deletions,
                    "total_changes": commit.stats.total
                })

                # Respect rate limits
                if len(commits) % 100 == 0:
                    rate_limit = self.get_rate_limit()
                    if rate_limit["core"]["remaining"] < 100:
                        wait_time = (rate_limit["core"]["reset"] - datetime.now(timezone.utc)).total_seconds()
                        if wait_time > 0:
                            print(f"Rate limit low. Waiting {int(wait_time)} seconds...")
                            time.sleep(wait_time)

            return commits
        except Exception as e:
            print(f"Error collecting commits for {repo_full_name}: {e}")
            return []

    def collect_pull_request_data(self, repo_full_name: str, since_days: int = 365,
                                    max_prs: int = 200) -> Dict[str, Any]:
        """
        Collect pull request data for coordination analysis.

        Args:
            repo_full_name: Repository in format "owner/repo"
            since_days: Number of days of history to collect
            max_prs: Maximum number of PRs to collect

        Returns:
            Dictionary containing PR statistics and samples
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            since_date = datetime.now(timezone.utc) - timedelta(days=since_days)

            prs_data = {
                "merged": [],
                "closed_unmerged": [],
                "open": [],
                "statistics": {
                    "total_prs": 0,
                    "merged_count": 0,
                    "closed_unmerged_count": 0,
                    "open_count": 0,
                    "avg_time_to_merge": 0,
                    "avg_time_to_close": 0,
                    "avg_comments_per_pr": 0,
                    "conflict_rate": 0
                }
            }

            # Collect closed/merged PRs
            closed_prs = repo.get_pulls(state='closed', sort='updated', direction='desc')
            merged_times = []
            closed_times = []
            total_comments = 0
            conflict_count = 0

            for i, pr in enumerate(tqdm(closed_prs, desc="Collecting PRs", total=min(max_prs, closed_prs.totalCount))):
                if i >= max_prs:
                    break

                if pr.updated_at < since_date:
                    break

                pr_data = {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "created_at": pr.created_at.isoformat(),
                    "updated_at": pr.updated_at.isoformat() if pr.updated_at else None,
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "author": pr.user.login if pr.user else None,
                    "comments": pr.comments,
                    "review_comments": pr.review_comments,
                    "commits": pr.commits,
                    "additions": pr.additions,
                    "deletions": pr.deletions,
                    "changed_files": pr.changed_files,
                    "mergeable_state": pr.mergeable_state,
                    "merged": pr.merged
                }

                total_comments += pr.comments + pr.review_comments

                # Check for merge conflicts
                if pr.mergeable_state in ['dirty', 'unstable']:
                    conflict_count += 1

                if pr.merged:
                    prs_data["merged"].append(pr_data)
                    if pr.merged_at and pr.created_at:
                        merge_time = (pr.merged_at - pr.created_at).total_seconds() / 3600  # hours
                        merged_times.append(merge_time)
                else:
                    prs_data["closed_unmerged"].append(pr_data)
                    if pr.closed_at and pr.created_at:
                        close_time = (pr.closed_at - pr.created_at).total_seconds() / 3600  # hours
                        closed_times.append(close_time)

                prs_data["statistics"]["total_prs"] += 1

                # Respect rate limits
                if i % 50 == 0:
                    rate_limit = self.get_rate_limit()
                    if rate_limit["core"]["remaining"] < 100:
                        wait_time = (rate_limit["core"]["reset"] - datetime.now(timezone.utc)).total_seconds()
                        if wait_time > 0:
                            print(f"Rate limit low. Waiting {int(wait_time)} seconds...")
                            time.sleep(wait_time)

            # Collect open PRs (sample)
            open_prs = repo.get_pulls(state='open', sort='created', direction='desc')
            for i, pr in enumerate(open_prs):
                if i >= 50:  # Limit open PRs sample
                    break

                prs_data["open"].append({
                    "number": pr.number,
                    "title": pr.title,
                    "created_at": pr.created_at.isoformat(),
                    "author": pr.user.login if pr.user else None,
                    "comments": pr.comments,
                    "review_comments": pr.review_comments
                })

            # Calculate statistics
            prs_data["statistics"]["merged_count"] = len(prs_data["merged"])
            prs_data["statistics"]["closed_unmerged_count"] = len(prs_data["closed_unmerged"])
            prs_data["statistics"]["open_count"] = len(prs_data["open"])

            if merged_times:
                prs_data["statistics"]["avg_time_to_merge"] = sum(merged_times) / len(merged_times)
            if closed_times:
                prs_data["statistics"]["avg_time_to_close"] = sum(closed_times) / len(closed_times)
            if prs_data["statistics"]["total_prs"] > 0:
                prs_data["statistics"]["avg_comments_per_pr"] = total_comments / prs_data["statistics"]["total_prs"]
                prs_data["statistics"]["conflict_rate"] = conflict_count / prs_data["statistics"]["total_prs"]

            return prs_data

        except Exception as e:
            print(f"Error collecting PRs for {repo_full_name}: {e}")
            return {"error": str(e), "statistics": {}}

    def collect_issue_data(self, repo_full_name: str, since_days: int = 365,
                           max_issues: int = 200) -> Dict[str, Any]:
        """
        Collect issue data for governance analysis.

        Args:
            repo_full_name: Repository in format "owner/repo"
            since_days: Number of days of history to collect
            max_issues: Maximum number of issues to collect

        Returns:
            Dictionary containing issue statistics and samples
        """
        try:
            repo = self.github.get_repo(repo_full_name)
            since_date = datetime.now(timezone.utc) - timedelta(days=since_days)

            issues_data = {
                "closed": [],
                "open": [],
                "statistics": {
                    "total_issues": 0,
                    "closed_count": 0,
                    "open_count": 0,
                    "avg_time_to_close": 0,
                    "avg_comments_per_issue": 0,
                    "bug_count": 0,
                    "enhancement_count": 0,
                    "question_count": 0
                }
            }

            # Collect closed issues
            closed_issues = repo.get_issues(state='closed', since=since_date)
            closed_times = []
            total_comments = 0
            label_counts = {"bug": 0, "enhancement": 0, "question": 0}

            for i, issue in enumerate(tqdm(closed_issues, desc="Collecting Issues", total=min(max_issues, closed_issues.totalCount))):
                if i >= max_issues:
                    break

                # Skip pull requests (GitHub API returns PRs with issues)
                if issue.pull_request:
                    continue

                labels = [label.name.lower() for label in issue.labels]

                issue_data = {
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "created_at": issue.created_at.isoformat(),
                    "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    "author": issue.user.login if issue.user else None,
                    "comments": issue.comments,
                    "labels": labels
                }

                issues_data["closed"].append(issue_data)
                total_comments += issue.comments

                # Categorize by labels
                if any('bug' in label for label in labels):
                    label_counts["bug"] += 1
                if any(term in label for label in labels for term in ['enhancement', 'feature']):
                    label_counts["enhancement"] += 1
                if any('question' in label for label in labels):
                    label_counts["question"] += 1

                if issue.closed_at and issue.created_at:
                    close_time = (issue.closed_at - issue.created_at).total_seconds() / 3600  # hours
                    closed_times.append(close_time)

                issues_data["statistics"]["total_issues"] += 1

                # Respect rate limits
                if i % 50 == 0:
                    rate_limit = self.get_rate_limit()
                    if rate_limit["core"]["remaining"] < 100:
                        wait_time = (rate_limit["core"]["reset"] - datetime.now(timezone.utc)).total_seconds()
                        if wait_time > 0:
                            print(f"Rate limit low. Waiting {int(wait_time)} seconds...")
                            time.sleep(wait_time)

            # Collect open issues (sample)
            open_issues = repo.get_issues(state='open', sort='created', direction='desc')
            for i, issue in enumerate(open_issues):
                if i >= 50:  # Limit open issues sample
                    break

                # Skip pull requests
                if issue.pull_request:
                    continue

                labels = [label.name.lower() for label in issue.labels]
                issues_data["open"].append({
                    "number": issue.number,
                    "title": issue.title,
                    "created_at": issue.created_at.isoformat(),
                    "author": issue.user.login if issue.user else None,
                    "comments": issue.comments,
                    "labels": labels
                })

            # Calculate statistics
            issues_data["statistics"]["closed_count"] = len(issues_data["closed"])
            issues_data["statistics"]["open_count"] = len(issues_data["open"])

            if closed_times:
                issues_data["statistics"]["avg_time_to_close"] = sum(closed_times) / len(closed_times)
            if issues_data["statistics"]["total_issues"] > 0:
                issues_data["statistics"]["avg_comments_per_issue"] = total_comments / issues_data["statistics"]["total_issues"]

            issues_data["statistics"]["bug_count"] = label_counts["bug"]
            issues_data["statistics"]["enhancement_count"] = label_counts["enhancement"]
            issues_data["statistics"]["question_count"] = label_counts["question"]

            return issues_data

        except Exception as e:
            print(f"Error collecting issues for {repo_full_name}: {e}")
            return {"error": str(e), "statistics": {}}

    def parse_maintainers_files(self, repo_full_name: str) -> List[str]:
        """
        Parse MAINTAINERS.md, CONTRIBUTORS.md, AUTHORS files for maintainer names.

        This is an alternative to the collaborators API which requires admin access.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            List of GitHub usernames found in maintainer files
        """
        maintainer_files = [
            "MAINTAINERS.md", "MAINTAINERS", "MAINTAINERS.txt",
            "CONTRIBUTORS.md", "CONTRIBUTORS", "CONTRIBUTORS.txt",
            "AUTHORS.md", "AUTHORS", "AUTHORS.txt",
            ".github/MAINTAINERS.md", ".github/CONTRIBUTORS.md"
        ]

        maintainers = set()
        repo = self.github.get_repo(repo_full_name)

        for file_path in maintainer_files:
            try:
                content_file = repo.get_contents(file_path)
                content = content_file.decoded_content.decode('utf-8')

                # Extract GitHub usernames using various patterns:
                # 1. @username format
                usernames = re.findall(r'@([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38})', content)
                maintainers.update(usernames)

                # 2. GitHub URLs: https://github.com/username
                github_urls = re.findall(r'github\.com/([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38})(?:/|\s|$)', content)
                maintainers.update(github_urls)

                # 3. Markdown links: [Name](https://github.com/username)
                markdown_links = re.findall(r'\[.*?\]\(https?://github\.com/([a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38})\)', content)
                maintainers.update(markdown_links)

                print(f"Found {len(maintainers)} maintainers in {file_path}")

            except Exception as e:
                # File doesn't exist or can't be read, continue
                continue

        # Filter out common false positives
        false_positives = {'github', 'issues', 'pulls', 'blob', 'tree', 'commit', 'raw',
                          'edit', 'settings', 'actions', 'security', 'wiki', 'projects'}
        maintainers = [m for m in maintainers if m.lower() not in false_positives]

        return list(maintainers)

    def collect_maintainer_data(self, repo_full_name: str) -> Dict[str, Any]:
        """
        Identify maintainers and their activity patterns.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            Dictionary with maintainer information
        """
        try:
            repo = self.github.get_repo(repo_full_name)

            maintainer_data = {
                "collaborators": [],
                "maintainers_from_files": [],
                "codeowners": None,
                "top_committers": [],
                "statistics": {
                    "total_collaborators": 0,
                    "maintainers_from_files_count": 0,
                    "active_maintainers_6mo": 0
                }
            }

            # Get collaborators (those with push access)
            try:
                collaborators = repo.get_collaborators()
                for collab in collaborators:
                    maintainer_data["collaborators"].append({
                        "login": collab.login,
                        "permissions": collab.permissions.__dict__ if hasattr(collab, 'permissions') else {}
                    })
                maintainer_data["statistics"]["total_collaborators"] = len(maintainer_data["collaborators"])
            except Exception as e:
                print(f"Could not fetch collaborators (requires admin access): {e}")
                print("Will use MAINTAINERS.md/CONTRIBUTORS.md files instead...")

            # Parse maintainer files (alternative to collaborators API)
            try:
                maintainers_from_files = self.parse_maintainers_files(repo_full_name)
                maintainer_data["maintainers_from_files"] = maintainers_from_files
                maintainer_data["statistics"]["maintainers_from_files_count"] = len(maintainers_from_files)
                if maintainers_from_files:
                    print(f"Found {len(maintainers_from_files)} maintainers from files: {maintainers_from_files}")
            except Exception as e:
                print(f"Could not parse maintainer files: {e}")

            # Try to get CODEOWNERS file
            try:
                codeowners_content = repo.get_contents(".github/CODEOWNERS")
                maintainer_data["codeowners"] = codeowners_content.decoded_content.decode('utf-8')
            except:
                try:
                    codeowners_content = repo.get_contents("CODEOWNERS")
                    maintainer_data["codeowners"] = codeowners_content.decoded_content.decode('utf-8')
                except:
                    pass

            # Get top committers from recent activity (proxy for active maintainers)
            since_date = datetime.now(timezone.utc) - timedelta(days=180)  # 6 months
            commit_authors = {}

            try:
                commits = repo.get_commits(since=since_date)
                for commit in commits:
                    if commit.author:
                        login = commit.author.login
                        commit_authors[login] = commit_authors.get(login, 0) + 1

                # Sort by commit count
                sorted_authors = sorted(commit_authors.items(), key=lambda x: x[1], reverse=True)
                maintainer_data["top_committers"] = [
                    {"login": author, "commits_6mo": count}
                    for author, count in sorted_authors[:10]
                ]
                maintainer_data["statistics"]["active_maintainers_6mo"] = len([
                    a for a, c in sorted_authors if c >= 5  # At least 5 commits in 6 months
                ])
            except Exception as e:
                print(f"Could not analyze committers: {e}")

            return maintainer_data

        except Exception as e:
            print(f"Error collecting maintainer data for {repo_full_name}: {e}")
            return {"error": str(e)}

    def check_governance_files(self, repo_full_name: str) -> Dict[str, bool]:
        """
        Check for presence of governance-related files.

        Args:
            repo_full_name: Repository in format "owner/repo"

        Returns:
            Dictionary indicating presence of governance files
        """
        governance_files = [
            "GOVERNANCE.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "MAINTAINERS.md",
            ".github/CODEOWNERS"
        ]

        results = {}
        repo = self.github.get_repo(repo_full_name)

        for file_path in governance_files:
            try:
                repo.get_contents(file_path)
                results[file_path] = True
            except:
                results[file_path] = False

        return results

    def save_data(self, data: Dict[str, Any], output_path: Path):
        """Save collected data to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        def json_serializer(obj):
            """Custom JSON serializer for non-serializable objects."""
            if hasattr(obj, '__dict__'):
                return str(obj)
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            return str(obj)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=json_serializer)
        print(f"Data saved to {output_path}")


    def collect_complete_dataset(self, repo_full_name: str, since_days: int = 365) -> Dict[str, Any]:
        """
        Collect complete dataset for a project.

        Args:
            repo_full_name: Repository in format "owner/repo"
            since_days: Number of days of history to collect

        Returns:
            Complete dataset dictionary
        """
        print(f"\n{'='*60}")
        print(f"Collecting complete dataset for: {repo_full_name}")
        print(f"{'='*60}\n")

        data = {
            "metadata": {
                "repo": repo_full_name,
                "collected_at": datetime.now(timezone.utc).isoformat(),
                "collection_period_days": since_days
            }
        }

        # Basic repository metrics
        print("1/7 Collecting repository metrics...")
        data["repository"] = self.collect_repository_metrics(repo_full_name)

        # Maintainer identification
        print("2/7 Identifying maintainers...")
        data["maintainers"] = self.collect_maintainer_data(repo_full_name)

        # Contributors
        print("3/7 Collecting contributor data...")
        data["contributors"] = self.collect_contributor_data(repo_full_name, max_contributors=100)

        # Commits
        print("4/7 Collecting commit history...")
        data["recent_commits"] = self.collect_commit_history(repo_full_name, since_days=since_days)

        # Pull requests
        print("5/7 Collecting pull request data...")
        data["pull_requests"] = self.collect_pull_request_data(repo_full_name, since_days=since_days)

        # Issues
        print("6/7 Collecting issue data...")
        data["issues"] = self.collect_issue_data(repo_full_name, since_days=since_days)

        # Governance files
        print("7/7 Checking governance files...")
        data["governance_files"] = self.check_governance_files(repo_full_name)

        print(f"\n{'='*60}")
        print(f"Collection complete for: {repo_full_name}")
        print(f"{'='*60}\n")

        return data


def main():
    """Example usage - collect data for a Stadium project."""
    import argparse

    parser = argparse.ArgumentParser(description='Collect GitHub data for OSS projects')
    parser.add_argument('repo', help='Repository in format owner/repo (e.g., curl/curl)')
    parser.add_argument('--days', type=int, default=365, help='Days of history to collect (default: 365)')
    parser.add_argument('--output-dir', default='data/raw', help='Output directory (default: data/raw)')

    args = parser.parse_args()

    collector = GitHubCollector()

    # Collect complete dataset
    data = collector.collect_complete_dataset(args.repo, since_days=args.days)

    # Save data
    output_path = Path(args.output_dir) / f"{args.repo.replace('/', '_')}_data.json"
    collector.save_data(data, output_path)

    # Print summary
    print("\n" + "="*60)
    print("COLLECTION SUMMARY")
    print("="*60)
    print(f"Repository: {args.repo}")
    print(f"Stars: {data['repository'].get('stargazers_count', 'N/A')}")
    print(f"Forks: {data['repository'].get('forks_count', 'N/A')}")
    print(f"Language: {data['repository'].get('language', 'N/A')}")
    print(f"\nMaintainers:")
    print(f"  - Collaborators: {data['maintainers']['statistics'].get('total_collaborators', 0)}")
    print(f"  - Active (6mo): {data['maintainers']['statistics'].get('active_maintainers_6mo', 0)}")
    print(f"\nContributors: {len(data['contributors'])}")
    print(f"Commits: {len(data['recent_commits'])}")
    print(f"\nPull Requests:")
    print(f"  - Total: {data['pull_requests']['statistics'].get('total_prs', 0)}")
    print(f"  - Merged: {data['pull_requests']['statistics'].get('merged_count', 0)}")
    print(f"  - Merge rate: {data['pull_requests']['statistics'].get('merged_count', 0) / max(data['pull_requests']['statistics'].get('total_prs', 1), 1) * 100:.1f}%")
    print(f"  - Avg time to merge: {data['pull_requests']['statistics'].get('avg_time_to_merge', 0):.1f} hours")
    print(f"  - Conflict rate: {data['pull_requests']['statistics'].get('conflict_rate', 0) * 100:.1f}%")
    print(f"\nIssues:")
    print(f"  - Total: {data['issues']['statistics'].get('total_issues', 0)}")
    print(f"  - Closed: {data['issues']['statistics'].get('closed_count', 0)}")
    print(f"  - Avg time to close: {data['issues']['statistics'].get('avg_time_to_close', 0):.1f} hours")
    print(f"\nGovernance files:")
    gov_files = [k for k, v in data['governance_files'].items() if v]
    if gov_files:
        for f in gov_files:
            print(f"  ✓ {f}")
    else:
        print("  - None found")

    print(f"\nData saved to: {output_path}")
    print(f"\nRate limit status:")
    rate_limit = collector.get_rate_limit()
    print(f"  - Core: {rate_limit['core']['remaining']}/{rate_limit['core']['limit']}")
    print(f"  - Reset: {rate_limit['core']['reset']}")
    print("="*60)


if __name__ == "__main__":
    main()
