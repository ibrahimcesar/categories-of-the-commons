"""
Entropy Calculation Module
Calculates organizational entropy across multiple dimensions.
"""

import numpy as np
from typing import List, Dict, Any
from scipy.stats import entropy as scipy_entropy


class EntropyCalculator:
    """Calculate entropy measures for OSS projects."""

    @staticmethod
    def shannon_entropy(probabilities: np.ndarray) -> float:
        """
        Calculate Shannon entropy.

        H = -Σ p(i) * log₂(p(i))

        Args:
            probabilities: Array of probability values

        Returns:
            Shannon entropy value
        """
        # Filter out zero probabilities
        p = probabilities[probabilities > 0]
        return -np.sum(p * np.log2(p))

    def contributor_entropy(self, contributor_data: List[Dict[str, Any]]) -> float:
        """
        Calculate contributor entropy from contribution distribution.

        H_contrib = -Σ p(contributor_i) * log₂(p(contributor_i))

        Args:
            contributor_data: List of dictionaries with 'login' and 'contributions' keys

        Returns:
            Contributor entropy value
        """
        if not contributor_data:
            return 0.0

        # Extract contribution counts
        contributions = np.array([c.get('contributions', 0) for c in contributor_data])
        total = contributions.sum()

        if total == 0:
            return 0.0

        # Calculate probability distribution
        probabilities = contributions / total

        return self.shannon_entropy(probabilities)

    def commit_temporal_entropy(self, commit_data: List[Dict[str, Any]], bins: int = 24) -> float:
        """
        Calculate temporal entropy from commit time distribution.

        Args:
            commit_data: List of commit dictionaries with 'date' field
            bins: Number of time bins (default 24 for hourly)

        Returns:
            Temporal entropy value
        """
        if not commit_data:
            return 0.0

        # Extract hour of day from commits
        from datetime import datetime
        hours = []
        for commit in commit_data:
            try:
                dt = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
                hours.append(dt.hour)
            except:
                continue

        if not hours:
            return 0.0

        # Create histogram
        hist, _ = np.histogram(hours, bins=bins, range=(0, 24))

        # Calculate probabilities
        probabilities = hist / hist.sum()

        return self.shannon_entropy(probabilities)

    def file_change_entropy(self, commit_data: List[Dict[str, Any]]) -> float:
        """
        Calculate entropy from file change patterns.

        Higher entropy = more diverse change patterns
        Lower entropy = concentrated changes

        Args:
            commit_data: List of commit dictionaries with change statistics

        Returns:
            File change entropy value
        """
        if not commit_data:
            return 0.0

        # Calculate change distribution (additions + deletions)
        changes = np.array([
            c.get('additions', 0) + c.get('deletions', 0)
            for c in commit_data
        ])

        if changes.sum() == 0:
            return 0.0

        # Bin changes into categories
        bins = [0, 10, 50, 200, 1000, np.inf]
        hist, _ = np.histogram(changes, bins=bins)

        # Calculate probabilities
        probabilities = hist / hist.sum()

        return self.shannon_entropy(probabilities)

    def calculate_all_entropy_measures(self, project_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate all entropy measures for a project.

        Args:
            project_data: Dictionary containing all project data

        Returns:
            Dictionary of entropy measures
        """
        return {
            "contributor_entropy": self.contributor_entropy(
                project_data.get('contributors', [])
            ),
            "temporal_entropy": self.commit_temporal_entropy(
                project_data.get('recent_commits', [])
            ),
            "change_entropy": self.file_change_entropy(
                project_data.get('recent_commits', [])
            )
        }

    def calculate_normalized_entropy(self, entropy_value: float, max_possible: float) -> float:
        """
        Normalize entropy to [0, 1] range.

        Args:
            entropy_value: Raw entropy value
            max_possible: Maximum possible entropy for this distribution

        Returns:
            Normalized entropy value
        """
        if max_possible == 0:
            return 0.0
        return entropy_value / max_possible


def main():
    """Example usage."""
    calculator = EntropyCalculator()

    # Example contributor data
    contributors = [
        {"login": "user1", "contributions": 500},
        {"login": "user2", "contributions": 200},
        {"login": "user3", "contributions": 100},
        {"login": "user4", "contributions": 50},
        {"login": "user5", "contributions": 10}
    ]

    entropy = calculator.contributor_entropy(contributors)
    print(f"Contributor entropy: {entropy:.3f} bits")

    # Maximum entropy would be when all contributors have equal contributions
    n = len(contributors)
    max_entropy = np.log2(n)
    normalized = calculator.calculate_normalized_entropy(entropy, max_entropy)
    print(f"Normalized entropy: {normalized:.3f} (max possible: {max_entropy:.3f})")


if __name__ == "__main__":
    main()
