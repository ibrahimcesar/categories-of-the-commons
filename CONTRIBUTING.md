# Contributing to Categories of the Commons

Thank you for your interest in contributing to this research project! This project investigates OSS governance using categorical theory, cybernetics, and information theory.

## Types of Contributions

### 1. Theoretical Feedback

**Categorical Framework**
- Critiques of the categorical formalization
- Suggestions for additional categorical structures
- Alternative interpretations of morphisms and functors

**Methodology**
- Improvements to entropy calculation methods
- Suggestions for VSM operationalization
- Statistical design critiques

### 2. Project Nominations

We're particularly interested in **Stadium projects** (high downloads, ≤3 maintainers) that would test our framework well.

**To nominate a project:**
1. Check it matches our criteria (see `data/projects.json`)
2. Open an issue with:
   - Repository URL
   - Project type (Stadium/Federation/Club/Control)
   - Why it's a good test case
   - Any special characteristics

**Stadium Project Criteria:**
- High download count (>100k/month for npm, >1M total for PyPI, etc.)
- ≤3 core maintainers
- Performance/usage data available
- Active (commits in last 6 months)

**Federation Project Criteria:**
- High user and contributor growth
- Established governance documentation
- Foundation backing (CNCF, Apache, Linux Foundation) preferred
- Multi-stakeholder decision-making

**Club Project Criteria:**
- Active niche community
- High contributor-to-user ratio
- Tight community cohesion
- Specialized domain

### 3. Data Validation

Help verify our classifications and measurements:
- Review project classifications (Stadium/Federation/Club)
- Validate entropy calculations
- Check VSM system mappings
- Verify Ostrom principle assessments

### 4. Code Contributions

**Areas needing development:**
- Additional data collectors (GitLab, Bitbucket, etc.)
- Enhanced entropy calculation methods
- Visualization improvements
- Statistical analysis enhancements

**Before coding:**
1. Check existing issues or open a new one
2. Discuss approach in the issue
3. Fork and create a feature branch
4. Follow our code style (see below)

### 5. Replication Attempts

Independent replication is highly valuable:
- Test our methodology on different samples
- Validate statistical findings
- Document discrepancies
- Suggest improvements

## Development Setup

### Prerequisites

- Python 3.10+
- Git
- GitHub personal access token (for data collection)

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/ibrahimcesar/categories-of-the-commons.git
cd categories-of-the-commons

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env and add your GitHub token

# Run tests
pytest

# Check code style
black --check src/
flake8 src/
mypy src/
```

## Code Style

We follow standard Python conventions:

- **Formatting:** [Black](https://black.readthedocs.io/) (line length 100)
- **Linting:** [Flake8](https://flake8.pycqa.org/)
- **Type hints:** [MyPy](https://mypy.readthedocs.io/)
- **Docstrings:** Google style

**Before committing:**
```bash
black src/
flake8 src/
mypy src/
pytest
```

## Project Structure

```
src/
├── collection/          # Data collection modules
│   ├── github_collector.py
│   ├── metrics_collector.py
│   └── governance_parser.py
├── analysis/            # Analysis modules
│   ├── entropy_calculation.py
│   ├── vsm_health.py
│   ├── ostrom_scoring.py
│   └── categorical_analysis.py
├── visualization/       # Plotting and visualization
└── utils/              # Helper utilities
```

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** with clear, atomic commits
4. **Write or update tests** as needed
5. **Update documentation** (README, docstrings, etc.)
6. **Ensure all tests pass**
7. **Submit a pull request** with:
   - Clear description of changes
   - Motivation and context
   - Related issues (if any)
   - Screenshots (for visualizations)

### PR Review Criteria

- Code follows style guidelines
- Tests pass
- Documentation updated
- Changes align with research goals
- No decrease in statistical power (for methodology changes)

## Research Ethics

This project analyzes **publicly available data only**:

- ✅ Public repository metrics
- ✅ Public commit history
- ✅ Public governance documents
- ✅ Public contributor information
- ❌ Private repositories
- ❌ Private communications
- ❌ Personal data not already public

If conducting interviews:
- Follow the protocol in `interviews/protocol.md`
- Obtain informed consent
- Anonymize transcripts
- Store securely

## Data Privacy

- **Never commit** API tokens, credentials, or private data
- **Use `.env`** for sensitive configuration
- **Anonymize** any interview data
- **Respect** repository licenses and terms of service

## Questions or Issues?

- **Theoretical questions:** Open a Discussion
- **Bug reports:** Open an Issue with "bug" label
- **Feature requests:** Open an Issue with "enhancement" label
- **Project nominations:** Open an Issue with "project nomination" label
- **General inquiries:** Email ibrahim@ibrahimcesar.com

## Academic Citation

If you build upon this work, please cite:

```bibtex
@misc{cesar2025categories,
  author = {Cesar, Ibrahim},
  title = {Categories of the Commons: From Cybernetics to Categorical
           Semantics in Distributed Software Organizations},
  year = {2025},
  institution = {University of São Paulo},
  note = {Independent Research / MBA Program},
  url = {https://github.com/ibrahimcesar/categories-of-the-commons}
}
```

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Acknowledgments

Contributors will be acknowledged in:
- The project README
- Academic paper (for substantial contributions)
- Release notes

Thank you for helping advance our understanding of OSS governance! 🙏
