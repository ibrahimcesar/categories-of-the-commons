# Quick Start Guide

Get up and running with Categories of the Commons research project in 5 minutes.

## 1. Setup (2 minutes)

```bash
# Clone and enter directory
git clone https://github.com/ibrahimcesar/categories-of-the-commons.git
cd categories-of-the-commons

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install
make install
# or: pip install -r requirements.txt && pip install -e .

# Configure
cp .env.example .env
# Edit .env and add your GitHub token from: https://github.com/settings/tokens
```

## 2. Verify Installation (1 minute)

```bash
# Check Python package
python -c "import src; print(f'Version: {src.__version__}')"

# Run tests
make test
# or: pytest

# Check code style
make check
# or: black src/ && flake8 src/
```

## 3. Collect Data (30 seconds)

```bash
# Collect data for a Stadium project (example: curl)
python src/collection/github_collector.py

# Check collected data
ls data/raw/
```

## 4. Calculate Entropy (30 seconds)

```bash
# Run entropy calculation example
python src/analysis/entropy_calculation.py
```

## 5. Explore (1 minute)

```bash
# Start Jupyter Lab
make notebooks
# or: jupyter lab

# Open: notebooks/01_data_exploration.ipynb
```

## Common Tasks

### Data Collection
```bash
make collect              # Run data collection
```

### Analysis
```bash
make analyze              # Run analysis pipeline
python -m src.analysis.entropy_calculation  # Calculate entropy
```

### Development
```bash
make format               # Format code with black
make lint                 # Run linting
make test                 # Run tests
make check                # Run all checks
```

### Project Management
```bash
# View project sample
cat data/projects.json

# Add new project nomination
# Edit data/projects.json and add to appropriate category
```

## Project Structure Overview

```
├── data/
│   ├── projects.json          # Stadium-optimized sample (n=70)
│   ├── raw/                   # Raw API data
│   └── processed/             # Cleaned datasets
├── src/
│   ├── collection/            # Data collectors (GitHub, etc.)
│   ├── analysis/              # Entropy, VSM, Ostrom, categorical
│   └── visualization/         # Plotting and figures
├── notebooks/                 # Jupyter analysis notebooks
├── results/                   # Tables, figures, reports
└── tests/                     # Unit tests
```

## Next Steps

1. **Review Research Design:** See [README.md](README.md#research-design-overview)
2. **Understand Sample:** Check [data/projects.json](data/projects.json)
3. **Explore Notebooks:** Start with `notebooks/01_data_exploration.ipynb`
4. **Contribute:** Read [CONTRIBUTING.md](CONTRIBUTING.md)

## Help & Support

- **Documentation:** See [README.md](README.md)
- **Issues:** https://github.com/ibrahimcesar/categories-of-the-commons/issues
- **Questions:** Open a Discussion or email ibrahim@ibrahimcesar.com

## Stadium-Focused Design

This project uses a **statistically optimized, Stadium-focused design**:
- **28-30 Stadium projects** (PRIMARY) - High downloads, ≤3 maintainers
- **12-15 Federation projects** (ANCHOR) - Established governance
- **8-10 Club projects** (CONVERGENT) - Tight communities
- **15-20 Control projects** (BASELINE) - Random sample

This design maximizes **categorical signal validity** and achieves **85% statistical power** for detecting medium effect sizes (d ≥ 0.50).

---

**Ready to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
