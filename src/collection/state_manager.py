"""
State Manager for GitHub Data Collection Daemon
Provides JSON-based state persistence for resumable batch collection.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import shutil


@dataclass
class CollectionState:
    """Represents the current state of collection."""
    pending: List[str]
    in_progress: Optional[str]
    completed: List[str]
    failed: List[Dict[str, str]]  # [{"repo": "owner/repo", "error": "message", "timestamp": "iso"}]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CollectionState':
        return cls(
            pending=data.get("pending", []),
            in_progress=data.get("in_progress"),
            completed=data.get("completed", []),
            failed=data.get("failed", [])
        )


class StateManager:
    """
    Manages collection state with atomic file operations.

    State file format:
    {
        "queue": {
            "pending": ["owner/repo1", ...],
            "in_progress": null,
            "completed": ["curl/curl", ...],
            "failed": [{"repo": "...", "error": "...", "timestamp": "..."}]
        },
        "metadata": {
            "created_at": "iso timestamp",
            "updated_at": "iso timestamp",
            "category": "stadium",
            "total_projects": 70
        },
        "statistics": {
            "api_calls_total": 0,
            "last_collection_duration_sec": 0
        }
    }
    """

    DEFAULT_STATE_PATH = Path("data/collection_state.json")

    def __init__(self, state_path: Optional[Path] = None):
        """
        Initialize state manager.

        Args:
            state_path: Path to state file. Defaults to data/collection_state.json
        """
        self.state_path = state_path or self.DEFAULT_STATE_PATH
        self._state: Optional[Dict[str, Any]] = None

    def _load_state(self) -> Dict[str, Any]:
        """Load state from file, creating default if doesn't exist."""
        if self.state_path.exists():
            with open(self.state_path, 'r') as f:
                return json.load(f)
        return self._default_state()

    def _default_state(self) -> Dict[str, Any]:
        """Create default empty state."""
        return {
            "queue": {
                "pending": [],
                "in_progress": None,
                "completed": [],
                "failed": []
            },
            "metadata": {
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "category": None,
                "total_projects": 0
            },
            "statistics": {
                "api_calls_total": 0,
                "last_collection_duration_sec": 0,
                "collections_completed": 0
            }
        }

    def _save_state(self, state: Dict[str, Any]) -> None:
        """
        Save state atomically using write-then-rename pattern.
        This prevents corruption if interrupted during write.
        """
        state["metadata"]["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Ensure directory exists
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file then rename (atomic on POSIX)
        temp_path = self.state_path.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            json.dump(state, f, indent=2)

        # Atomic rename
        shutil.move(str(temp_path), str(self.state_path))

    @property
    def state(self) -> Dict[str, Any]:
        """Get current state (lazy loaded)."""
        if self._state is None:
            self._state = self._load_state()
        return self._state

    def refresh(self) -> None:
        """Force reload state from disk."""
        self._state = self._load_state()

    def initialize(self, projects: List[str], category: str) -> None:
        """
        Initialize collection queue with a list of projects.

        Args:
            projects: List of repo strings in "owner/repo" format
            category: Category name (stadium, federation, club, toy)
        """
        # Check if there's existing state with in-progress work
        if self.state_path.exists():
            existing = self._load_state()
            if existing["queue"]["in_progress"] or existing["queue"]["pending"]:
                raise ValueError(
                    f"Existing state found with {len(existing['queue']['pending'])} pending "
                    f"and in_progress={existing['queue']['in_progress']}. "
                    f"Use 'resume' or delete state file first."
                )

        state = self._default_state()
        state["queue"]["pending"] = projects
        state["metadata"]["category"] = category
        state["metadata"]["total_projects"] = len(projects)

        self._save_state(state)
        self._state = state

        print(f"✅ Initialized queue with {len(projects)} projects for category '{category}'")

    def add_projects(self, projects: List[str], skip_existing: bool = True) -> int:
        """
        Add projects to the pending queue.

        Args:
            projects: List of repo strings to add
            skip_existing: If True, skip projects already in any queue

        Returns:
            Number of projects actually added
        """
        state = self.state
        existing = set(state["queue"]["pending"]) | set(state["queue"]["completed"])
        existing |= {f["repo"] for f in state["queue"]["failed"]}
        if state["queue"]["in_progress"]:
            existing.add(state["queue"]["in_progress"])

        added = 0
        for project in projects:
            if skip_existing and project in existing:
                continue
            state["queue"]["pending"].append(project)
            existing.add(project)
            added += 1

        state["metadata"]["total_projects"] = (
            len(state["queue"]["pending"]) +
            len(state["queue"]["completed"]) +
            len(state["queue"]["failed"]) +
            (1 if state["queue"]["in_progress"] else 0)
        )

        self._save_state(state)
        return added

    def get_next(self) -> Optional[str]:
        """
        Get next project to collect. Marks it as in_progress.

        Returns:
            Next project repo string, or None if queue is empty
        """
        state = self.state

        # If something is already in progress, return it
        if state["queue"]["in_progress"]:
            return state["queue"]["in_progress"]

        # Get next from pending
        if not state["queue"]["pending"]:
            return None

        next_project = state["queue"]["pending"].pop(0)
        state["queue"]["in_progress"] = next_project

        self._save_state(state)
        return next_project

    def mark_completed(self, repo: str) -> None:
        """
        Mark a project as successfully collected.

        Args:
            repo: Repository string that was collected
        """
        state = self.state

        if state["queue"]["in_progress"] == repo:
            state["queue"]["in_progress"] = None

        if repo not in state["queue"]["completed"]:
            state["queue"]["completed"].append(repo)

        state["statistics"]["collections_completed"] += 1
        self._save_state(state)

    def mark_failed(self, repo: str, error: str) -> None:
        """
        Mark a project as failed.

        Args:
            repo: Repository string that failed
            error: Error message
        """
        state = self.state

        if state["queue"]["in_progress"] == repo:
            state["queue"]["in_progress"] = None

        state["queue"]["failed"].append({
            "repo": repo,
            "error": error,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        self._save_state(state)

    def retry_failed(self) -> int:
        """
        Move all failed projects back to pending queue.

        Returns:
            Number of projects moved to pending
        """
        state = self.state

        failed_repos = [f["repo"] for f in state["queue"]["failed"]]
        state["queue"]["pending"].extend(failed_repos)
        state["queue"]["failed"] = []

        self._save_state(state)
        return len(failed_repos)

    def update_statistics(self, api_calls: int = 0, duration_sec: float = 0) -> None:
        """Update collection statistics."""
        state = self.state
        state["statistics"]["api_calls_total"] += api_calls
        if duration_sec > 0:
            state["statistics"]["last_collection_duration_sec"] = duration_sec
        self._save_state(state)

    def get_status(self) -> Dict[str, Any]:
        """
        Get current collection status summary.

        Returns:
            Dictionary with status information
        """
        state = self.state

        total = state["metadata"]["total_projects"]
        pending = len(state["queue"]["pending"])
        completed = len(state["queue"]["completed"])
        failed = len(state["queue"]["failed"])
        in_progress = 1 if state["queue"]["in_progress"] else 0

        return {
            "category": state["metadata"]["category"],
            "total": total,
            "pending": pending,
            "in_progress": state["queue"]["in_progress"],
            "completed": completed,
            "failed": failed,
            "progress_pct": (completed / total * 100) if total > 0 else 0,
            "created_at": state["metadata"]["created_at"],
            "updated_at": state["metadata"]["updated_at"],
            "statistics": state["statistics"]
        }

    def get_queue(self) -> CollectionState:
        """Get the queue as a CollectionState object."""
        return CollectionState.from_dict(self.state["queue"])

    def clear(self) -> None:
        """Clear all state (delete state file)."""
        if self.state_path.exists():
            os.remove(self.state_path)
        self._state = None
        print(f"✅ Cleared state file: {self.state_path}")


def main():
    """Test state manager functionality."""
    import tempfile

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        test_path = Path(f.name)

    try:
        manager = StateManager(test_path)

        # Initialize
        projects = ["curl/curl", "nodejs/node", "kubernetes/kubernetes"]
        manager.initialize(projects, "stadium")

        print("\nInitial status:")
        print(manager.get_status())

        # Get and complete first
        next_proj = manager.get_next()
        print(f"\nGot next: {next_proj}")
        manager.mark_completed(next_proj)

        # Get and fail second
        next_proj = manager.get_next()
        print(f"Got next: {next_proj}")
        manager.mark_failed(next_proj, "Rate limit exceeded")

        print("\nAfter operations:")
        print(manager.get_status())

        # Retry failed
        retried = manager.retry_failed()
        print(f"\nRetried {retried} failed projects")
        print(manager.get_status())

    finally:
        test_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
