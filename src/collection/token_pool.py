"""
Token Pool Manager for GitHub API Rate Limit Handling
Manages multiple GitHub tokens for increased throughput and automatic rotation.
"""

import os
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import requests


@dataclass
class TokenInfo:
    """Information about a single GitHub token."""
    token: str
    token_id: str  # Identifier like "token_0", "token_1"
    remaining: int = 5000
    limit: int = 5000
    reset_at: Optional[datetime] = None
    last_checked: Optional[datetime] = None

    def is_available(self, min_remaining: int = 100) -> bool:
        """Check if token has enough remaining calls."""
        return self.remaining >= min_remaining

    def seconds_until_reset(self) -> float:
        """Get seconds until rate limit resets."""
        if not self.reset_at:
            return 0
        delta = self.reset_at - datetime.now(timezone.utc)
        return max(0, delta.total_seconds())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token_id": self.token_id,
            "remaining": self.remaining,
            "limit": self.limit,
            "reset_at": self.reset_at.isoformat() if self.reset_at else None,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None
        }


class TokenPool:
    """
    Manages a pool of GitHub tokens for rate limit handling.

    Supports:
    - Single token from GITHUB_TOKEN env var
    - Multiple tokens from GITHUB_TOKENS env var (comma-separated)
    - Automatic rotation to token with most remaining calls
    - Wait time calculation when all tokens exhausted
    """

    def __init__(
        self,
        tokens: Optional[List[str]] = None,
        min_remaining: int = 100
    ):
        """
        Initialize token pool.

        Args:
            tokens: List of GitHub tokens. If None, reads from environment.
            min_remaining: Minimum remaining calls to consider a token usable.
        """
        self.min_remaining = min_remaining
        self.tokens: List[TokenInfo] = []
        self._current_index = 0

        # Load tokens
        if tokens:
            token_list = tokens
        else:
            token_list = self._load_from_env()

        for i, token in enumerate(token_list):
            self.tokens.append(TokenInfo(
                token=token,
                token_id=f"token_{i}"
            ))

        if not self.tokens:
            raise ValueError(
                "No GitHub tokens found. Set GITHUB_TOKEN or GITHUB_TOKENS environment variable."
            )

        print(f"✅ Token pool initialized with {len(self.tokens)} token(s)")

    def _load_from_env(self) -> List[str]:
        """Load tokens from environment variables."""
        tokens = []

        # Try GITHUB_TOKENS first (comma-separated for multiple)
        multi_tokens = os.getenv("GITHUB_TOKENS", "")
        if multi_tokens:
            tokens = [t.strip() for t in multi_tokens.split(",") if t.strip()]

        # Fall back to single GITHUB_TOKEN
        if not tokens:
            single_token = os.getenv("GITHUB_TOKEN", "")
            if single_token:
                tokens = [single_token]

        return tokens

    def _check_rate_limit(self, token_info: TokenInfo) -> None:
        """
        Check and update rate limit for a token.

        Args:
            token_info: TokenInfo object to update
        """
        try:
            response = requests.get(
                "https://api.github.com/rate_limit",
                headers={
                    "Authorization": f"token {token_info.token}",
                    "Accept": "application/vnd.github.v3+json"
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                core = data["resources"]["core"]

                token_info.remaining = core["remaining"]
                token_info.limit = core["limit"]
                token_info.reset_at = datetime.fromtimestamp(core["reset"], tz=timezone.utc)
                token_info.last_checked = datetime.now(timezone.utc)

            elif response.status_code == 401:
                print(f"⚠️  Token {token_info.token_id} is invalid or expired")
                token_info.remaining = 0
            else:
                print(f"⚠️  Rate limit check failed for {token_info.token_id}: {response.status_code}")

        except Exception as e:
            print(f"⚠️  Error checking rate limit for {token_info.token_id}: {e}")

    def refresh_all(self) -> None:
        """Check rate limits for all tokens."""
        for token_info in self.tokens:
            self._check_rate_limit(token_info)
            time.sleep(0.1)  # Small delay between checks

    def get_best_token(self) -> Optional[Tuple[str, TokenInfo]]:
        """
        Get the token with the most remaining API calls.

        Returns:
            Tuple of (token_string, TokenInfo) or None if all exhausted
        """
        # Refresh rate limits
        self.refresh_all()

        # Sort by remaining calls (descending)
        available = [t for t in self.tokens if t.is_available(self.min_remaining)]

        if not available:
            return None

        best = max(available, key=lambda t: t.remaining)
        return (best.token, best)

    def get_token(self) -> Optional[str]:
        """
        Get a usable token (simple interface).

        Returns:
            Token string or None if all exhausted
        """
        result = self.get_best_token()
        return result[0] if result else None

    def get_any_token(self) -> str:
        """
        Get any token (even if rate limited).
        Used for initializing collectors.

        Returns:
            First available token string
        """
        return self.tokens[0].token

    def update_remaining(self, token: str, remaining: int, reset_at: Optional[datetime] = None) -> None:
        """
        Update remaining calls for a token after API usage.
        Call this after making API requests.

        Args:
            token: Token string used
            remaining: New remaining count
            reset_at: Optional new reset time
        """
        for token_info in self.tokens:
            if token_info.token == token:
                token_info.remaining = remaining
                if reset_at:
                    token_info.reset_at = reset_at
                token_info.last_checked = datetime.now(timezone.utc)
                break

    def decrement_remaining(self, token: str, count: int = 1) -> None:
        """
        Decrement remaining calls (estimate without API check).

        Args:
            token: Token string used
            count: Number of calls made
        """
        for token_info in self.tokens:
            if token_info.token == token:
                token_info.remaining = max(0, token_info.remaining - count)
                break

    def get_wait_time(self) -> float:
        """
        Get seconds to wait until any token is available.

        Returns:
            Seconds until soonest reset, or 0 if a token is available
        """
        # Check if any token is already available
        for token_info in self.tokens:
            if token_info.is_available(self.min_remaining):
                return 0

        # Find soonest reset
        reset_times = [t.seconds_until_reset() for t in self.tokens if t.reset_at]
        if not reset_times:
            return 3600  # Default 1 hour if unknown

        return min(reset_times) + 60  # Add 60s buffer

    def get_total_remaining(self) -> int:
        """Get total remaining calls across all tokens."""
        return sum(t.remaining for t in self.tokens)

    def get_status(self) -> Dict[str, Any]:
        """
        Get status of all tokens.

        Returns:
            Dictionary with token pool status
        """
        return {
            "token_count": len(self.tokens),
            "total_remaining": self.get_total_remaining(),
            "min_remaining_threshold": self.min_remaining,
            "any_available": any(t.is_available(self.min_remaining) for t in self.tokens),
            "wait_time_seconds": self.get_wait_time(),
            "tokens": {t.token_id: t.to_dict() for t in self.tokens}
        }

    def print_status(self) -> None:
        """Print human-readable token status."""
        print("\n" + "=" * 50)
        print("TOKEN POOL STATUS")
        print("=" * 50)

        for t in self.tokens:
            available = "✅" if t.is_available(self.min_remaining) else "❌"
            reset_str = ""
            if t.reset_at and not t.is_available(self.min_remaining):
                mins = t.seconds_until_reset() / 60
                reset_str = f" (resets in {mins:.0f}m)"

            print(f"{available} {t.token_id}: {t.remaining}/{t.limit}{reset_str}")

        print("-" * 50)
        print(f"Total remaining: {self.get_total_remaining()}")

        wait = self.get_wait_time()
        if wait > 0:
            print(f"Wait time: {wait/60:.0f} minutes")
        else:
            print("Ready to collect!")
        print("=" * 50 + "\n")


def main():
    """Test token pool functionality."""
    from dotenv import load_dotenv

    load_dotenv()

    pool = TokenPool()
    pool.refresh_all()
    pool.print_status()

    # Test getting best token
    result = pool.get_best_token()
    if result:
        token, info = result
        print(f"Best token: {info.token_id} with {info.remaining} remaining")
    else:
        print(f"No tokens available. Wait {pool.get_wait_time()/60:.0f} minutes.")


if __name__ == "__main__":
    main()
