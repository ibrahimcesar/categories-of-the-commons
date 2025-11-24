.PHONY: help install test lint format clean docs

help:
	@echo "Categories of the Commons - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies and setup environment"
	@echo "  make install-dev  Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test         Run tests with pytest"
	@echo "  make lint         Run linting (flake8, mypy)"
	@echo "  make format       Format code with black"
	@echo "  make check        Run all checks (lint + test)"
	@echo ""
	@echo "Data:"
	@echo "  make collect      Run data collection scripts"
	@echo "  make analyze      Run analysis pipeline"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         Build documentation"
	@echo "  make notebooks    Start Jupyter Lab"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        Remove temporary files and caches"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev,docs,notebooks]"

test:
	pytest -v --cov=src tests/

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

check: lint test

collect:
	@echo "Running data collection..."
	python src/collection/github_collector.py

analyze:
	@echo "Running analysis pipeline..."
	python src/analysis/entropy_calculation.py

docs:
	cd docs && sphinx-build -b html . _build/

notebooks:
	jupyter lab

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ htmlcov/ .coverage
	@echo "Cleaned up temporary files"
