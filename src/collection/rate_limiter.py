"""
Intelligent Rate Limiter for GitHub Data Collection
Wraps token pool with smart waiting and progress display.
"""

import time
import sys
from datetime import datetime, timezone
from typing import Optional, Callable, Any
from dataclasses import dataclass

from .token_pool import TokenPool


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting behavior."""
    min_remaining: int = 500  # Stop collecting when below this
    calls_per_project_estimate: int = 350  # Estimated API calls per project
    wait_buffer_seconds: int = 60  # Extra seconds after reset
    progress_update_interval: int = 30  # Seconds between progress updates during wait
    max_wait_time: int = 3700  # Max seconds to wait (slightly over 1 hour)


class RateLimiter:
    """
    Intelligent rate limiter with automatic waiting and progress display.

    Features:
    - Wraps TokenPool for seamless token rotation
    - Estimates if enough calls remain for a project
    - Waits with progress bar when rate limited
    - Graceful handling of interrupts during wait
    """

    def __init__(
        self,
        token_pool: Optional[TokenPool] = None,
        config: Optional[RateLimitConfig] = None,
        on_wait_start: Optional[Callable[[float], None]] = None,
        on_wait_complete: Optional[Callable[[], None]] = None
    ):
        """
        Initialize rate limiter.

        Args:
            token_pool: TokenPool instance. Created automatically if None.
            config: Rate limit configuration.
            on_wait_start: Callback when starting to wait. Receives wait time in seconds.
            on_wait_complete: Callback when wait completes.
        """
        self.pool = token_pool or TokenPool()
        self.config = config or RateLimitConfig()
        self.on_wait_start = on_wait_start
        self.on_wait_complete = on_wait_complete

        self._interrupted = False

    def can_collect(self, refresh: bool = True) -> bool:
        """
        Check if we have enough remaining calls to collect a project.

        Args:
            refresh: If True, refresh rate limits from API first.

        Returns:
            True if collection can proceed, False if should wait.
        """
        if refresh:
            self.pool.refresh_all()

        return self.pool.get_total_remaining() >= self.config.min_remaining

    def can_collect_n_projects(self, n: int, refresh: bool = True) -> bool:
        """
        Check if we have enough calls for N projects.

        Args:
            n: Number of projects to collect
            refresh: If True, refresh rate limits first

        Returns:
            True if enough calls remain
        """
        if refresh:
            self.pool.refresh_all()

        needed = n * self.config.calls_per_project_estimate
        return self.pool.get_total_remaining() >= needed

    def estimate_projects_possible(self) -> int:
        """
        Estimate how many projects can be collected with current limits.

        Returns:
            Estimated number of projects
        """
        remaining = self.pool.get_total_remaining()
        usable = remaining - self.config.min_remaining
        return max(0, usable // self.config.calls_per_project_estimate)

    def get_token(self) -> Optional[str]:
        """
        Get a usable token.

        Returns:
            Token string or None if all exhausted
        """
        return self.pool.get_token()

    def wait_for_reset(self, interactive: bool = True) -> bool:
        """
        Wait until rate limit resets.

        Args:
            interactive: If True, show progress. If False, just sleep.

        Returns:
            True if wait completed, False if interrupted
        """
        self._interrupted = False
        wait_time = self.pool.get_wait_time()

        if wait_time <= 0:
            return True

        # Clamp to max wait time
        wait_time = min(wait_time, self.config.max_wait_time)

        if self.on_wait_start:
            self.on_wait_start(wait_time)

        if interactive:
            return self._interactive_wait(wait_time)
        else:
            time.sleep(wait_time)
            if self.on_wait_complete:
                self.on_wait_complete()
            return True

    def _interactive_wait(self, wait_time: float) -> bool:
        """
        Wait with progress display.

        Args:
            wait_time: Seconds to wait

        Returns:
            True if completed, False if interrupted
        """
        start_time = time.time()
        end_time = start_time + wait_time

        print(f"\n⏳ Rate limit reached. Waiting {wait_time/60:.0f} minutes...")
        print("   Press Ctrl+C to stop and save progress.\n")

        try:
            while time.time() < end_time and not self._interrupted:
                elapsed = time.time() - start_time
                remaining = wait_time - elapsed
                progress = elapsed / wait_time * 100

                # Format time remaining
                mins = int(remaining // 60)
                secs = int(remaining % 60)

                # Create progress bar
                bar_width = 30
                filled = int(bar_width * progress / 100)
                bar = "█" * filled + "░" * (bar_width - filled)

                # Print progress (overwrite line)
                sys.stdout.write(f"\r   [{bar}] {progress:.0f}% - {mins}m {secs}s remaining")
                sys.stdout.flush()

                time.sleep(min(1, remaining))

            print()  # New line after progress

            if self._interrupted:
                print("   ⚠️  Wait interrupted by user")
                return False

            if self.on_wait_complete:
                self.on_wait_complete()

            print("   ✅ Rate limit reset! Resuming collection...\n")
            return True

        except KeyboardInterrupt:
            print("\n   ⚠️  Wait interrupted by user")
            self._interrupted = True
            return False

    def interrupt(self) -> None:
        """Signal to interrupt waiting."""
        self._interrupted = True

    def ensure_can_collect(self, interactive: bool = True) -> bool:
        """
        Ensure we can collect, waiting if necessary.

        Args:
            interactive: Show progress during wait

        Returns:
            True if can collect, False if interrupted or timed out
        """
        if self.can_collect(refresh=True):
            return True

        return self.wait_for_reset(interactive=interactive) and self.can_collect(refresh=True)

    def report_usage(self, calls_made: int, token: Optional[str] = None) -> None:
        """
        Report API usage after collection.

        Args:
            calls_made: Number of API calls made
            token: Token used (for accurate tracking)
        """
        if token:
            self.pool.decrement_remaining(token, calls_made)

    def get_status(self) -> dict:
        """Get comprehensive status."""
        return {
            "can_collect": self.can_collect(refresh=False),
            "total_remaining": self.pool.get_total_remaining(),
            "projects_possible": self.estimate_projects_possible(),
            "wait_time_minutes": self.pool.get_wait_time() / 60,
            "token_count": len(self.pool.tokens),
            "config": {
                "min_remaining": self.config.min_remaining,
                "calls_per_project": self.config.calls_per_project_estimate
            }
        }

    def print_status(self) -> None:
        """Print human-readable status."""
        self.pool.refresh_all()

        print("\n" + "=" * 50)
        print("RATE LIMIT STATUS")
        print("=" * 50)

        remaining = self.pool.get_total_remaining()
        possible = self.estimate_projects_possible()
        can_collect = self.can_collect(refresh=False)

        print(f"Total remaining: {remaining:,} API calls")
        print(f"Minimum threshold: {self.config.min_remaining}")
        print(f"Estimated calls/project: {self.config.calls_per_project_estimate}")
        print(f"Projects possible: ~{possible}")
        print()

        if can_collect:
            print("✅ Ready to collect!")
        else:
            wait = self.pool.get_wait_time()
            print(f"❌ Rate limit low. Wait {wait/60:.0f} minutes.")

        print("=" * 50 + "\n")

        # Also show token breakdown
        self.pool.print_status()


def main():
    """Test rate limiter functionality."""
    from dotenv import load_dotenv
    load_dotenv()

    limiter = RateLimiter()
    limiter.print_status()

    print(f"\nCan collect: {limiter.can_collect()}")
    print(f"Projects possible: {limiter.estimate_projects_possible()}")


if __name__ == "__main__":
    main()
