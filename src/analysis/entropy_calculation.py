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

    def contributor_entropy(self, contributor_data: List[Dict[str, Any]]) -> tuple:
        """
        Calculate contributor entropy from contribution distribution.

        H_contrib = -Σ p(contributor_i) * log₂(p(contributor_i))

        Args:
            contributor_data: List of dictionaries with 'login' and 'contributions' keys

        Returns:
            Tuple of (entropy, normalized_entropy)
        """
        if not contributor_data:
            return 0.0, 0.0

        # Extract contribution counts
        contributions = np.array([c.get('contributions', 0) for c in contributor_data])
        total = contributions.sum()

        if total == 0:
            return 0.0, 0.0

        # Calculate probability distribution
        probabilities = contributions / total

        # Calculate entropy
        entropy = self.shannon_entropy(probabilities)

        # Calculate normalized entropy (0 = concentrated, 1 = uniform)
        max_entropy = np.log2(len(contributor_data))
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return entropy, normalized_entropy

    @staticmethod
    def gini_coefficient(values: List[float]) -> float:
        """
        Calculate Gini coefficient for inequality measurement.

        0 = perfect equality (everyone contributes equally)
        1 = perfect inequality (one person does everything)

        Args:
            values: List of contribution values

        Returns:
            Gini coefficient between 0 and 1
        """
        if not values or len(values) == 0:
            return 0.0

        values = np.array(values, dtype=float)
        values = values[values > 0]  # Remove zeros

        if len(values) == 0:
            return 0.0

        # Sort values
        sorted_values = np.sort(values)
        n = len(sorted_values)

        # Calculate Gini using the formula: G = (2 * Σ(i * x_i) - (n + 1) * Σx_i) / (n * Σx_i)
        cumulative_sum = np.cumsum(sorted_values)
        gini = (2 * np.sum(np.arange(1, n + 1) * sorted_values) - (n + 1) * cumulative_sum[-1]) / (n * cumulative_sum[-1])

        return gini

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
        contributors = project_data.get('contributors', [])
        entropy, normalized_entropy = self.contributor_entropy(contributors)

        # Calculate Gini coefficient
        contributions = [c.get('contributions', 0) for c in contributors]
        gini = self.gini_coefficient(contributions)

        return {
            "contributor_entropy": entropy,
            "contributor_entropy_normalized": normalized_entropy,
            "contributor_gini": gini,
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

    def classify_project(self, contributor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Classify project using refined Stadium criteria.

        Based on curl/curl analysis, Stadium projects exhibit DOMINANCE patterns:
        1. Top contributor dominance > 40%
        2. High Gini coefficient > 0.8
        3. Low normalized entropy < 0.6

        A project is Stadium if it meets 2 of 3 criteria.

        Args:
            contributor_data: List of contributor dictionaries

        Returns:
            Dictionary with classification and metrics
        """
        if not contributor_data:
            return {
                "classification": "Unknown",
                "confidence": 0.0,
                "metrics": {},
                "criteria_met": []
            }

        # Calculate metrics
        entropy, normalized_entropy = self.contributor_entropy(contributor_data)
        contributions = [c.get('contributions', 0) for c in contributor_data]
        total = sum(contributions)

        if total == 0:
            return {
                "classification": "Unknown",
                "confidence": 0.0,
                "metrics": {},
                "criteria_met": []
            }

        top1_pct = contributions[0] / total * 100
        top2_pct = sum(contributions[:2]) / total * 100 if len(contributions) >= 2 else top1_pct
        gini = self.gini_coefficient(contributions)

        # Evaluate refined Stadium criteria
        criteria_met = []

        # Criterion 1: Top contributor dominance > 40%
        if top1_pct > 40:
            criteria_met.append("top_contributor_dominance")

        # Criterion 2: High Gini coefficient > 0.8
        if gini > 0.8:
            criteria_met.append("high_gini")

        # Criterion 3: Low normalized entropy < 0.6
        if normalized_entropy < 0.6:
            criteria_met.append("low_entropy")

        # Classification based on criteria
        stadium_score = len(criteria_met)

        if stadium_score >= 3:
            classification = "Stadium (Strong)"
            confidence = 0.95
        elif stadium_score >= 2:
            classification = "Stadium (Likely)"
            confidence = 0.75
        elif stadium_score >= 1:
            classification = "Hybrid/Uncertain"
            confidence = 0.50
        else:
            classification = "Federation/Club"
            confidence = 0.70

        return {
            "classification": classification,
            "confidence": confidence,
            "stadium_score": stadium_score,
            "criteria_met": criteria_met,
            "metrics": {
                "entropy": entropy,
                "normalized_entropy": normalized_entropy,
                "gini_coefficient": gini,
                "top_contributor_pct": top1_pct,
                "top_2_contributors_pct": top2_pct,
                "total_contributors": len(contributor_data)
            }
        }


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

    entropy, normalized = calculator.contributor_entropy(contributors)
    print(f"Contributor entropy: {entropy:.3f} bits")
    print(f"Normalized entropy: {normalized:.3f} (0=concentrated, 1=uniform)")

    # Calculate Gini coefficient
    contributions = [c['contributions'] for c in contributors]
    gini = calculator.gini_coefficient(contributions)
    print(f"Gini coefficient: {gini:.3f} (0=equal, 1=concentrated)")


if __name__ == "__main__":
    main()
