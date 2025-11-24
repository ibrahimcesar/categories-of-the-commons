"""
GitHub Data Collector
Collects repository metrics, commits, PRs, issues, and contributor data from GitHub API.
"""

import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

import requests
from github import Github, RateLimitExceededException
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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

        self.github = Github(self.token)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        })

    def get_rate_limit(self) -> Dict[str, Any]:
        """Get current GitHub API rate limit status."""
        rate_limit = self.github.get_rate_limit()
        return {
            "core": {
                "remaining": rate_limit.core.remaining,
                "limit": rate_limit.core.limit,
                "reset": rate_limit.core.reset
            },
            "search": {
                "remaining": rate_limit.search.remaining,
                "limit": rate_limit.search.limit,
                "reset": rate_limit.search.reset
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
                "collected_at": datetime.now().isoformat()
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
            since_date = datetime.now() - timedelta(days=since_days)
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
                        wait_time = (rate_limit["core"]["reset"] - datetime.now()).seconds
                        print(f"Rate limit low. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)

            return commits
        except Exception as e:
            print(f"Error collecting commits for {repo_full_name}: {e}")
            return []

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
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {output_path}")


def main():
    """Example usage."""
    collector = GitHubCollector()

    # Example: Collect data for curl (Stadium project)
    repo_name = "curl/curl"
    print(f"Collecting data for {repo_name}...")

    data = {
        "repository": collector.collect_repository_metrics(repo_name),
        "contributors": collector.collect_contributor_data(repo_name, max_contributors=50),
        "governance_files": collector.check_governance_files(repo_name),
        "recent_commits": collector.collect_commit_history(repo_name, since_days=90)
    }

    output_path = Path("data/raw") / f"{repo_name.replace('/', '_')}_data.json"
    collector.save_data(data, output_path)

    print("Rate limit status:", collector.get_rate_limit())


if __name__ == "__main__":
    main()
