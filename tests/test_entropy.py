"""
Tests for entropy calculation module.
"""

import pytest
import numpy as np
from src.analysis.entropy_calculation import EntropyCalculator


class TestEntropyCalculator:
    """Test suite for EntropyCalculator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = EntropyCalculator()

    def test_shannon_entropy_uniform(self):
        """Test Shannon entropy with uniform distribution (maximum entropy)."""
        # Uniform distribution: all probabilities equal
        probs = np.array([0.25, 0.25, 0.25, 0.25])
        entropy = self.calculator.shannon_entropy(probs)

        # Maximum entropy for 4 elements is log2(4) = 2.0
        assert np.isclose(entropy, 2.0, rtol=1e-5)

    def test_shannon_entropy_deterministic(self):
        """Test Shannon entropy with deterministic distribution (minimum entropy)."""
        # Deterministic: one probability is 1, rest are 0
        probs = np.array([1.0, 0.0, 0.0, 0.0])
        entropy = self.calculator.shannon_entropy(probs)

        # Minimum entropy is 0
        assert np.isclose(entropy, 0.0, rtol=1e-5)

    def test_contributor_entropy_equal(self):
        """Test contributor entropy with equal contributions."""
        contributors = [
            {"login": "user1", "contributions": 100},
            {"login": "user2", "contributions": 100},
            {"login": "user3", "contributions": 100},
            {"login": "user4", "contributions": 100}
        ]
        entropy = self.calculator.contributor_entropy(contributors)

        # Should be maximum entropy: log2(4) = 2.0
        assert np.isclose(entropy, 2.0, rtol=1e-5)

    def test_contributor_entropy_single(self):
        """Test contributor entropy with single dominant contributor."""
        contributors = [
            {"login": "user1", "contributions": 1000},
            {"login": "user2", "contributions": 1},
            {"login": "user3", "contributions": 1},
            {"login": "user4", "contributions": 1}
        ]
        entropy = self.calculator.contributor_entropy(contributors)

        # Should be very low entropy (close to 0)
        assert entropy < 0.5

    def test_contributor_entropy_empty(self):
        """Test contributor entropy with empty data."""
        entropy = self.calculator.contributor_entropy([])
        assert entropy == 0.0

    def test_normalize_entropy(self):
        """Test entropy normalization."""
        entropy_value = 1.5
        max_possible = 3.0
        normalized = self.calculator.calculate_normalized_entropy(entropy_value, max_possible)

        assert np.isclose(normalized, 0.5, rtol=1e-5)

    def test_normalize_entropy_zero_max(self):
        """Test entropy normalization with zero maximum."""
        normalized = self.calculator.calculate_normalized_entropy(1.0, 0.0)
        assert normalized == 0.0
