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


def get_uncollected(category: str) -> list:
    """Get list of uncollected candidates for a category."""
    if category == "stadium":
        return [c for c in STADIUM_ALL if c not in STADIUM_COLLECTED]
    elif category == "federation":
        return [c for c in FEDERATION_CANDIDATES if c not in FEDERATION_COLLECTED]
    elif category == "club":
        return [c for c in CLUB_CANDIDATES if c not in CLUB_COLLECTED]
    elif category == "toy":
        return [c for c in TOY_CANDIDATES if c not in TOY_COLLECTED]
    return []


def print_status():
    """Print collection status for all categories."""
    print("=" * 50)
    print("CANDIDATE COLLECTION STATUS")
    print("=" * 50)
    for cat, status in COLLECTION_STATUS.items():
        pct = (status["collected"] / status["total"] * 100) if status["total"] > 0 else 0
        print(f"{cat.upper():12} {status['collected']:3}/{status['total']:3} ({pct:.0f}%)")
    print("=" * 50)
