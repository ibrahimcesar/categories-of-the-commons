#!/usr/bin/env python3
"""
GitHub Data Collection Daemon CLI
Resumable batch collection with rate limit management.

Usage:
    # Initialize queue from candidates
    python -m src.collection.collector_daemon init --category stadium

    # Start/continue collection (stops at rate limit)
    python -m src.collection.collector_daemon collect --limit 10

    # Check status
    python -m src.collection.collector_daemon status

    # Resume after waiting
    python -m src.collection.collector_daemon resume

    # Retry failed projects
    python -m src.collection.collector_daemon retry

    # Clear state and start fresh
    python -m src.collection.collector_daemon clear
"""

import argparse
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .state_manager import StateManager
from .token_pool import TokenPool
from .rate_limiter import RateLimiter, RateLimitConfig
from .github_collector import GitHubCollector


class CollectorDaemon:
    """
    Main daemon for automated GitHub data collection.

    Handles:
    - Queue management via StateManager
    - Rate limit handling via RateLimiter
    - Graceful shutdown on SIGINT/SIGTERM
    - Progress tracking and reporting
    """

    def __init__(
        self,
        state_path: Optional[Path] = None,
        output_dir: Optional[Path] = None,
        since_days: int = 365
    ):
        """
        Initialize collector daemon.

        Args:
            state_path: Path to state file
            output_dir: Directory for output data
            since_days: Days of history to collect
        """
        self.state_manager = StateManager(state_path)
        self.output_dir = output_dir or Path("data/raw")
        self.since_days = since_days

        # Will be initialized lazily
        self._token_pool: Optional[TokenPool] = None
        self._rate_limiter: Optional[RateLimiter] = None
        self._collector: Optional[GitHubCollector] = None

        # Shutdown flag
        self._shutdown_requested = False

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print("\n\n⚠️  Shutdown requested. Saving progress...")
        self._shutdown_requested = True

        if self._rate_limiter:
            self._rate_limiter.interrupt()

    @property
    def token_pool(self) -> TokenPool:
        """Lazy initialization of token pool."""
        if self._token_pool is None:
            self._token_pool = TokenPool()
        return self._token_pool

    @property
    def rate_limiter(self) -> RateLimiter:
        """Lazy initialization of rate limiter."""
        if self._rate_limiter is None:
            config = RateLimitConfig(
                min_remaining=500,
                calls_per_project_estimate=350,
                wait_buffer_seconds=60
            )
            self._rate_limiter = RateLimiter(
                token_pool=self.token_pool,
                config=config
            )
        return self._rate_limiter

    @property
    def collector(self) -> GitHubCollector:
        """Lazy initialization of GitHub collector."""
        if self._collector is None:
            token = self.token_pool.get_any_token()
            self._collector = GitHubCollector(token=token)
        return self._collector

    def init_queue(self, category: str, include_collected: bool = False) -> None:
        """
        Initialize collection queue from candidate list.

        Args:
            category: Category name (stadium, federation, club, toy)
            include_collected: If True, include already collected projects
        """
        # Import candidates
        from data.candidates import ALL_CANDIDATES, get_uncollected

        if category not in ALL_CANDIDATES:
            print(f"❌ Unknown category: {category}")
            print(f"   Available: {', '.join(ALL_CANDIDATES.keys())}")
            sys.exit(1)

        if include_collected:
            projects = ALL_CANDIDATES[category]
        else:
            projects = get_uncollected(category)

        if not projects:
            print(f"✅ All {category} projects already collected!")
            return

        self.state_manager.initialize(projects, category)

        print(f"\n📋 Queue initialized:")
        print(f"   Category: {category}")
        print(f"   Projects: {len(projects)}")
        print(f"   Estimated API calls: {len(projects) * 350:,}")
        print(f"   Estimated time: {len(projects) * 350 / 5000:.1f} hours (single token)")

    def collect(
        self,
        limit: Optional[int] = None,
        wait_on_limit: bool = False,
        interactive: bool = True
    ) -> dict:
        """
        Run collection for pending projects.

        Args:
            limit: Maximum projects to collect this run
            wait_on_limit: If True, wait for rate limit reset and continue
            interactive: Show progress output

        Returns:
            Summary of collection run
        """
        start_time = time.time()
        collected = 0
        failed = 0

        status = self.state_manager.get_status()
        if status["pending"] == 0 and not status["in_progress"]:
            print("✅ No pending projects to collect!")
            return {"collected": 0, "failed": 0, "reason": "queue_empty"}

        print(f"\n🚀 Starting collection...")
        print(f"   Pending: {status['pending']}")
        print(f"   Limit: {limit or 'unlimited'}")
        print(f"   Wait on limit: {wait_on_limit}")
        print()

        while not self._shutdown_requested:
            # Check if we've hit our limit
            if limit and collected >= limit:
                print(f"\n✅ Reached collection limit ({limit})")
                break

            # Get next project
            project = self.state_manager.get_next()
            if not project:
                print("\n✅ Queue empty - collection complete!")
                break

            # Check rate limit
            if not self.rate_limiter.can_collect():
                if wait_on_limit:
                    print(f"\n⏳ Rate limit low. Current project: {project}")
                    if not self.rate_limiter.wait_for_reset(interactive=interactive):
                        print("   Wait interrupted. Progress saved.")
                        break
                else:
                    print(f"\n⏸️  Rate limit low. Stopping collection.")
                    print(f"   Use 'resume' command to continue later.")
                    break

            # Collect project
            try:
                print(f"📥 [{collected + 1}] Collecting: {project}")

                data = self.collector.collect_complete_dataset(
                    project,
                    since_days=self.since_days
                )

                # Save data
                output_path = self.output_dir / f"{project.replace('/', '_')}_data.json"
                self.collector.save_data(data, output_path)

                # Mark completed
                self.state_manager.mark_completed(project)
                collected += 1

                # Brief status
                if "repository" in data:
                    stars = data["repository"].get("stargazers_count", "?")
                    contributors = len(data.get("contributors", []))
                    print(f"   ✅ Saved: ⭐ {stars} | 👥 {contributors} contributors")

            except Exception as e:
                error_msg = str(e)
                print(f"   ❌ Failed: {error_msg}")
                self.state_manager.mark_failed(project, error_msg)
                failed += 1

            # Update rate limiter with estimated usage
            self.rate_limiter.report_usage(350)

        # Final summary
        duration = time.time() - start_time
        self.state_manager.update_statistics(
            api_calls=collected * 350,
            duration_sec=duration
        )

        return {
            "collected": collected,
            "failed": failed,
            "duration_seconds": duration,
            "reason": "shutdown" if self._shutdown_requested else "complete"
        }

    def resume(self, **kwargs) -> dict:
        """Resume collection from where it left off."""
        return self.collect(**kwargs)

    def retry_failed(self) -> None:
        """Move failed projects back to pending queue."""
        count = self.state_manager.retry_failed()
        if count:
            print(f"✅ Moved {count} failed projects back to pending queue")
        else:
            print("ℹ️  No failed projects to retry")

    def print_status(self) -> None:
        """Print detailed status."""
        status = self.state_manager.get_status()

        print("\n" + "=" * 60)
        print("COLLECTION STATUS")
        print("=" * 60)

        print(f"\n📊 Queue Status:")
        print(f"   Category: {status['category'] or 'Not initialized'}")
        print(f"   Total projects: {status['total']}")
        print(f"   Pending: {status['pending']}")
        print(f"   Completed: {status['completed']} ({status['progress_pct']:.1f}%)")
        print(f"   Failed: {status['failed']}")
        if status['in_progress']:
            print(f"   In progress: {status['in_progress']}")

        if status['statistics']:
            stats = status['statistics']
            print(f"\n📈 Statistics:")
            print(f"   API calls total: {stats.get('api_calls_total', 0):,}")
            print(f"   Collections completed: {stats.get('collections_completed', 0)}")
            if stats.get('last_collection_duration_sec'):
                mins = stats['last_collection_duration_sec'] / 60
                print(f"   Last run duration: {mins:.1f} minutes")

        print(f"\n⏱️  Timestamps:")
        print(f"   Created: {status['created_at']}")
        print(f"   Updated: {status['updated_at']}")

        # Rate limit status
        print()
        self.rate_limiter.print_status()

    def clear(self, force: bool = False) -> None:
        """Clear collection state."""
        status = self.state_manager.get_status()

        if not force and (status['in_progress'] or status['pending'] > 0):
            print("⚠️  Queue has pending work:")
            print(f"   In progress: {status['in_progress']}")
            print(f"   Pending: {status['pending']}")
            print("   Use --force to clear anyway")
            return

        self.state_manager.clear()

    def add_projects(self, projects: list) -> None:
        """Add specific projects to queue."""
        added = self.state_manager.add_projects(projects)
        print(f"✅ Added {added} projects to queue")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="GitHub Data Collection Daemon",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize queue for stadium category
  python -m src.collection.collector_daemon init --category stadium

  # Collect up to 10 projects
  python -m src.collection.collector_daemon collect --limit 10

  # Collect and wait for rate limit resets
  python -m src.collection.collector_daemon collect --wait

  # Check current status
  python -m src.collection.collector_daemon status

  # Retry failed projects
  python -m src.collection.collector_daemon retry
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # init command
    init_parser = subparsers.add_parser("init", help="Initialize collection queue")
    init_parser.add_argument(
        "--category", "-c",
        required=True,
        choices=["stadium", "federation", "club", "toy"],
        help="Category to collect"
    )
    init_parser.add_argument(
        "--include-collected",
        action="store_true",
        help="Include already collected projects"
    )

    # collect command
    collect_parser = subparsers.add_parser("collect", help="Run collection")
    collect_parser.add_argument(
        "--limit", "-n",
        type=int,
        help="Maximum projects to collect"
    )
    collect_parser.add_argument(
        "--wait", "-w",
        action="store_true",
        help="Wait for rate limit reset and continue"
    )
    collect_parser.add_argument(
        "--days", "-d",
        type=int,
        default=365,
        help="Days of history to collect (default: 365)"
    )

    # resume command
    resume_parser = subparsers.add_parser("resume", help="Resume collection")
    resume_parser.add_argument("--limit", "-n", type=int)
    resume_parser.add_argument("--wait", "-w", action="store_true")
    resume_parser.add_argument("--days", "-d", type=int, default=365)

    # status command
    subparsers.add_parser("status", help="Show collection status")

    # retry command
    subparsers.add_parser("retry", help="Retry failed projects")

    # clear command
    clear_parser = subparsers.add_parser("clear", help="Clear collection state")
    clear_parser.add_argument("--force", "-f", action="store_true")

    # add command
    add_parser = subparsers.add_parser("add", help="Add specific projects")
    add_parser.add_argument("projects", nargs="+", help="Projects in owner/repo format")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Create daemon
    daemon = CollectorDaemon(
        since_days=getattr(args, 'days', 365)
    )

    # Execute command
    if args.command == "init":
        daemon.init_queue(args.category, args.include_collected)

    elif args.command == "collect":
        result = daemon.collect(
            limit=args.limit,
            wait_on_limit=args.wait
        )
        print(f"\n📊 Collection Summary:")
        print(f"   Collected: {result['collected']}")
        print(f"   Failed: {result['failed']}")
        print(f"   Duration: {result['duration_seconds']/60:.1f} minutes")

    elif args.command == "resume":
        result = daemon.resume(
            limit=args.limit,
            wait_on_limit=args.wait
        )
        print(f"\n📊 Resume Summary:")
        print(f"   Collected: {result['collected']}")
        print(f"   Failed: {result['failed']}")

    elif args.command == "status":
        daemon.print_status()

    elif args.command == "retry":
        daemon.retry_failed()

    elif args.command == "clear":
        daemon.clear(force=args.force)

    elif args.command == "add":
        daemon.add_projects(args.projects)


if __name__ == "__main__":
    main()
