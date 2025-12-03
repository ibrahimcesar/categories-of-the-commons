"""
Candidate lists for each governance category.
Import these for batch collection and analysis.
"""

from .stadium_candidates import (
    COLLECTED as STADIUM_COLLECTED,
    HIGH_PRIORITY as STADIUM_HIGH_PRIORITY,
    MEDIUM_PRIORITY as STADIUM_MEDIUM_PRIORITY,
    ALL_CANDIDATES as STADIUM_ALL,
)

from .federation_candidates import (
    CANDIDATES as FEDERATION_CANDIDATES,
    HIGH_PRIORITY as FEDERATION_HIGH_PRIORITY,
    COLLECTED as FEDERATION_COLLECTED,
)

from .club_candidates import (
    CANDIDATES as CLUB_CANDIDATES,
    HIGH_PRIORITY as CLUB_HIGH_PRIORITY,
    COLLECTED as CLUB_COLLECTED,
)

from .toy_candidates import (
    CANDIDATES as TOY_CANDIDATES,
    HIGH_PRIORITY as TOY_HIGH_PRIORITY,
    COLLECTED as TOY_COLLECTED,
)

# Master list of all candidates by category
ALL_CANDIDATES = {
    "stadium": STADIUM_ALL,
    "federation": FEDERATION_CANDIDATES,
    "club": CLUB_CANDIDATES,
    "toy": TOY_CANDIDATES,
}

# Collection status
COLLECTION_STATUS = {
    "stadium": {"collected": len(STADIUM_COLLECTED), "total": len(STADIUM_ALL)},
    "federation": {"collected": len(FEDERATION_COLLECTED), "total": len(FEDERATION_CANDIDATES)},
    "club": {"collected": len(CLUB_COLLECTED), "total": len(CLUB_CANDIDATES)},
    "toy": {"collected": len(TOY_COLLECTED), "total": len(TOY_CANDIDATES)},
}


def get_actually_collected() -> set:
    """Get set of actually collected projects by checking data/raw/ directory."""
    import os
    from pathlib import Path

    raw_dir = Path(__file__).parent.parent / "raw"
    collected = set()

    if raw_dir.exists():
        for f in raw_dir.glob("*_data.json"):
            # Convert filename back to owner/repo format
            name = f.stem.replace("_data", "")
            # Replace first underscore with slash (owner_repo -> owner/repo)
            parts = name.split("_", 1)
            if len(parts) == 2:
                collected.add(f"{parts[0]}/{parts[1]}")

    return collected


def get_uncollected(category: str) -> list:
    """Get list of uncollected candidates for a category by checking actual files."""
    actually_collected = get_actually_collected()

    candidates = ALL_CANDIDATES.get(category, [])
    return [c for c in candidates if c not in actually_collected]


def print_status():
    """Print collection status for all categories (checks actual files)."""
    actually_collected = get_actually_collected()

    print("=" * 50)
    print("CANDIDATE COLLECTION STATUS")
    print("=" * 50)
    for cat, candidates in ALL_CANDIDATES.items():
        collected_count = len([c for c in candidates if c in actually_collected])
        total = len(candidates)
        pct = (collected_count / total * 100) if total > 0 else 0
        status_icon = "✅" if collected_count == total else "🔄"
        print(f"{status_icon} {cat.upper():12} {collected_count:3}/{total:3} ({pct:.0f}%)")
    print("=" * 50)
