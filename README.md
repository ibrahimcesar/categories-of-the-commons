<div align="center">

# Categories of the Commons

**From Cybernetics to Categorical Semantics in Distributed Software Organizations**

*Formalizing Organizational Viability in Open Source Software Governance*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Research](https://img.shields.io/badge/Type-Academic%20Research-blue.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-green.svg)]()

</div>

---

> *"The limits of my language mean the limits of my world."*  
> — Ludwig Wittgenstein, *Philosophical Investigations*

---

## Abstract

Open source software (OSS) represents one of the most successful examples of commons-based peer production in human history. Yet we lack formal frameworks for understanding why some OSS projects thrive while others collapse, why certain governance structures enable sustainability while others lead to burnout and abandonment.

This research develops a **categorical-cybernetic framework** for analyzing OSS governance, synthesizing:

- **Stafford Beer's Viable System Model (VSM)** — organizational cybernetics
- **Elinor Ostrom's Institutional Analysis** — commons governance principles
- **Nadia Asparouhova's OSS Taxonomy** — contemporary open source typology
- **Category Theory** — formal compositional semantics
- **Sheaf Theory & Čech Cohomology** — local-to-global governance coherence

We operationalize this framework through **entropy measurement** on publicly available OSS data, testing whether categorical structure predicts project viability across different governance models.

**Keywords:** Open Source Software, Commons Governance, Category Theory, Cybernetics, Viable System Model, Institutional Analysis, Organizational Entropy

---

## Research Design Overview

This research employs a **statistically optimized, Stadium-focused design** that prioritizes categorical signal validity over traditional balanced sampling:

**Sample Allocation:**
- **Stadium Projects (n=28-30):** PRIMARY focus - high downloads, ≤3 maintainers, maximum categorical signal
- **Federation Projects (n=12-15):** THEORETICAL ANCHOR - established governance baseline
- **Club Projects (n=8-10):** CONVERGENT CASE - low entropy validation
- **Control Group (n=15-20):** BASELINE - statistical noise estimation

**Key Innovation:** Rather than equally sampling all project types, we concentrate on **Stadium projects** where organizational constraints create the clearest categorical structure. Stadium projects represent **terminal objects** in the organizational constraint category—the limit case of viable operation under minimal human resources. This makes them ideal for testing whether organizational structure (functors) actually reduces entropy (target category).

**Expected Results:**
- Large effect sizes (d > 0.8) for Stadium entropy vs other types
- Statistical power ≥ 0.85 with α = 0.05
- Differential Ostrom applicability (predicts Federations but not Stadiums)
- Observable functorial preservation in constrained organizations

This design maximizes both **statistical power** and **theoretical validity** by aligning sample allocation with the categorical structure being investigated.

---

## 📋 Project Planning

- **[TODO.md](TODO.md)** - Comprehensive task list organized by phase and priority
- **[ROADMAP.md](ROADMAP.md)** - Timeline, milestones, and weekly progress tracking
- **[QUICK_START.md](QUICK_START.md)** - 5-minute setup guide for contributors

---

## Table of Contents

- [Research Design Overview](#research-design-overview)
- [Research Questions](#research-questions)
- [Theoretical Framework](#theoretical-framework)
  - [The Four Project Types](#the-four-project-types)
  - [Viable System Model for OSS](#viable-system-model-for-oss)
  - [Ostrom's Design Principles](#ostroms-design-principles)
  - [Categorical Formalization](#categorical-formalization)
  - [Sheaf-Theoretic Framework](#sheaf-theoretic-framework)
  - [Entropy as Viability Indicator](#entropy-as-viability-indicator)
- [Methodology](#methodology)
  - [Data Sources](#data-sources)
  - [Sample Selection](#sample-selection)
  - [Statistical Design Rationale](#statistical-design-rationale)
  - [Information-Theoretic Justification](#information-theoretic-justification)
  - [Measurement Framework](#measurement-framework)
  - [Analysis Plan](#analysis-plan)
  - [Expected Statistical Outcomes](#expected-statistical-outcomes)
- [Key Hypotheses](#key-hypotheses)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Development](#development)
- [Repository Structure](#repository-structure)
- [Timeline](#timeline)
- [Contributing](#contributing)
- [Related Work](#related-work)
- [Author](#author)
- [Citation](#citation)
- [License](#license)

---

## Research Questions

**RQ1: Taxonomic Structure**  
Do different OSS project types (Federations, Stadiums, Clubs, Toys) exhibit systematically different categorical structures in their governance?

**RQ2: Ostrom Applicability**  
Does Ostrom's framework predict viability for collective-action projects (Federations, Clubs) but fail for individual-maintainer projects (Stadiums)? What predicts Stadium viability?

**RQ3: VSM Operationalization**  
Can Viable System Model health be measured from public OSS data (commits, PRs, issues, governance documents), and does it predict sustainability?

**RQ4: Entropy Dynamics**  
Do entropy patterns differ by project type? Do entropy trajectories predict governance crises before they manifest?

**RQ5: Categorical Unification**  
Is there a unified categorical framework that explains viability conditions across all project types?

---

## Theoretical Framework

### The Four Project Types

Following Nadia Asparouhova's taxonomy in *Working in Public* (2020), we classify OSS projects along two axes:

```
                        CONTRIBUTOR GROWTH
                        Low              High
                    ┌─────────────┬─────────────┐
               High │   STADIUM   │ FEDERATION  │
      USER          │             │             │
     GROWTH         ├─────────────┼─────────────┤
               Low  │    TOYS     │    CLUB     │
                    │             │             │
                    └─────────────┴─────────────┘
```

| Type | Users | Contributors | Examples | Governance Challenge |
|------|-------|--------------|----------|---------------------|
| **Federation** | High | High | Linux, Kubernetes, Rust | Coordination at scale |
| **Stadium** | High | Low | curl, core-js, Babel | Maintainer sustainability |
| **Club** | Low | High | Niche frameworks, academic projects | Maintaining coherence |
| **Toy** | Low | Low | Personal projects | None (individual) |

Each type faces different viability threats and requires different analytical approaches.

### Viable System Model for OSS

Stafford Beer's VSM identifies five systems necessary for organizational viability:

```
┌─────────────────────────────────────────────────────────────┐
│                    ENVIRONMENT                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 SYSTEM 5: POLICY                      │  │
│  │     Identity, Values, Strategic Direction             │  │
│  │     [GOVERNANCE.md, Mission, Core Values]             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               SYSTEM 4: INTELLIGENCE                  │  │
│  │     Environmental Scanning, Future Planning           │  │
│  │     [Roadmaps, RFCs, Ecosystem Monitoring]            │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     SYSTEM 3: CONTROL     │    SYSTEM 3*: AUDIT       │  │
│  │     Operational Oversight │    Direct Verification    │  │
│  │     [Metrics, Releases]   │    [Security Audits]      │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               SYSTEM 2: COORDINATION                  │  │
│  │     Conflict Resolution, Standards, Anti-oscillation  │  │
│  │     [CONTRIBUTING.md, CI/CD, Code Review]             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               SYSTEM 1: OPERATIONS                    │  │
│  │     Primary Activities, Value Creation                │  │
│  │     [Development, Commits, PRs, Releases]             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**VSM in OSS Context:**

| System | Function | OSS Manifestation | Measurable Indicators |
|--------|----------|-------------------|----------------------|
| S1 | Operations | Development activity | Commit frequency, PR merge rate, release cadence |
| S2 | Coordination | Conflict prevention | PR conflict rate, review turnaround, contributor guidelines |
| S3 | Control | Oversight | CI/CD coverage, test coverage, metrics dashboards |
| S3* | Audit | Verification | Security audits, architecture reviews, vulnerability response |
| S4 | Intelligence | Environment scanning | Dependency updates, ecosystem engagement, roadmap activity |
| S5 | Policy | Identity & direction | Governance clarity, mission coherence, decision consistency |

### Ostrom's Design Principles

Elinor Ostrom's Nobel Prize-winning research identified eight principles for sustainable commons governance:

| # | Principle | OSS Interpretation | Applicable To |
|---|-----------|-------------------|---------------|
| 1 | **Clearly Defined Boundaries** | Who has commit access? Who is a maintainer? | All types |
| 2 | **Congruence** | Rules fit project's technical/social reality | All types |
| 3 | **Collective-Choice Arrangements** | Affected parties participate in rule-making | Federations, Clubs |
| 4 | **Monitoring** | Compliance is observable (CI/CD, reviews) | Federations, Clubs |
| 5 | **Graduated Sanctions** | Proportional responses to violations | Federations |
| 6 | **Conflict Resolution** | Low-cost dispute resolution mechanisms | Federations, Clubs |
| 7 | **Recognition of Rights** | External authorities respect self-governance | Federations |
| 8 | **Nested Enterprises** | Multi-scale governance (SIGs, WGs) | Federations |

**Key Insight:** Ostrom's framework applies fully to **Federations**, partially to **Clubs**, and poorly to **Stadiums**. Stadiums lack the collective-action structure Ostrom's framework assumes.

### Categorical Formalization

We model OSS governance categorically:

**Definition (OSS Governance Category).** A governed OSS project is a category **C** where:

- **Objects:** Contributors, repositories, issues, PRs, releases, governance bodies
- **Morphisms:** Contribution flows, review relationships, merge operations, governance decisions
- **Composition:** Sequential governance operations (issue → PR → review → merge → release)
- **Identity:** Maintainer self-approval, automatic CI checks

**Definition (Governance Functor).** A governance model is a functor G: **Activity** → **Outcome** mapping development activities to project states, preserving compositional structure.

**Definition (Viability).** A project is *viable* iff:
1. All VSM systems have corresponding functorial representations
2. The governance functor preserves limits (conflicts resolve)
3. Entropy remains within sustainable bounds over time

**Key Categorical Structures:**

| Structure | OSS Interpretation |
|-----------|-------------------|
| **Product** | Parallel development streams that must integrate |
| **Coproduct** | Alternative approaches (forks, competing PRs) |
| **Pullback** | Merge operations reconciling divergent branches |
| **Pushout** | Feature integration from multiple sources |
| **Limit** | Consensus formation, conflict resolution |
| **Colimit** | Community growth, scope expansion |
| **Adjunction** | Governance ⊣ Autonomy balance |

**The Specification ⊣ Freedom Adjunction:**

```
Governance: Project ⇄ Constrained_Project : Freedom
```

Too much governance (left adjoint dominates): Contributors leave, forks emerge
Too much freedom (right adjoint dominates): Quality degrades, coherence collapses

Healthy projects oscillate within this adjunction.

### Sheaf-Theoretic Framework

We extend the categorical approach using **sheaf theory** to capture local-to-global governance coherence. See [theory/sheaf-cohomology-framework.md](theory/sheaf-cohomology-framework.md) for the complete mathematical treatment.

**Key Concepts:**

| Sheaf Concept | OSS Governance Interpretation |
|---------------|-------------------------------|
| **Base Space** | Project topology (contributors, modules, time) |
| **Stalks** | Local governance data (contributor knowledge, commit context) |
| **Sections** | Consistent governance rules across regions |
| **Gluing Axiom** | Local decisions must combine into coherent global policy |
| **Čech Cohomology** | Measures governance coherence and conflict |

**Cohomology Interpretation:**

| Cohomology Group | Meaning |
|------------------|---------|
| **H⁰** | Global governance consensus (universal rules) |
| **H¹** | Governance conflicts (incompatible local policies) |
| **H²** | Structural obstructions (deep incompatibilities, fork precursors) |

**The Cohomological Health Index:**

$$\chi_{\text{gov}}(X) = \dim H^0 - \dim H^1 + \dim H^2$$

This Euler characteristic-like invariant correlates with project sustainability metrics.

**Key Hypothesis:** Non-trivial H² classes (structural governance incompatibilities) precede fork events by 6-12 months—providing a predictive signal for governance crises.

### Entropy as Viability Indicator

We measure organizational entropy across multiple dimensions:

**Configuration Entropy:** Variation in code style, architecture, conventions
```
H_config = -Σ p(pattern_i) log₂ p(pattern_i)
```

**Contributor Entropy:** Distribution of contributions across participants
```
H_contrib = -Σ p(contributor_i) log₂ p(contributor_i)
```

**Governance Entropy:** Consistency in decision-making processes
```
H_gov = -Σ p(decision_type_i) log₂ p(decision_type_i)
```

**Temporal Entropy:** Predictability of development patterns over time

**Entropy Interpretation:**

| Entropy Level | Interpretation | Risk |
|---------------|----------------|------|
| Very Low | Rigid, single-maintainer dominated | Bus factor, stagnation |
| Low-Moderate | Consistent, well-governed | Healthy |
| Moderate-High | Diverse, experimental | Creative but coordination-costly |
| Very High | Chaotic, fragmented | Governance collapse |

**Organizational Breathing:** Healthy projects oscillate between entropy states:
- **Expansion phase:** High entropy (experimentation, growth, inclusion)
- **Consolidation phase:** Low entropy (standardization, documentation, cleanup)

Projects that get stuck in either phase face viability threats.

---

## Methodology

### Data Sources

All data is publicly available:

| Source | Data Type | Access Method |
|--------|-----------|---------------|
| GitHub/GitLab | Commits, PRs, issues, contributors | REST/GraphQL API |
| Package registries | Downloads, dependents | npm, PyPI, crates.io APIs |
| Governance docs | GOVERNANCE.md, CONTRIBUTING.md | Repository files |
| Communication | Discussions, mailing lists | Platform APIs |
| Metrics | OpenSSF Scorecard, CHAOSS | Public dashboards |

### Sample Selection

**Statistically Optimized Design** prioritizing signal-to-noise ratio and categorical coherence:

| Quadrant | Sample | Selection Criteria | Rationale |
|----------|--------|-------------------|-----------|
| **Stadium** | 28-30 | High downloads, ≤3 maintainers, performance data available | **PRIMARY**: Maximum categorical signal under organizational constraint |
| **Federation** | 12-15 | CNCF/Apache/LF projects with established governance | **THEORETICAL ANCHOR**: Baseline entropy, functorial structure validation |
| **Club** | 8-10 | Active niche communities, tight coherence | **CONVERGENT CASE**: Low entropy validation, strong organizational morphisms |
| **Control** | 15-20 | Random sampling across types | **BASELINE**: Statistical noise estimate |

**Total: ~60-75 projects**

#### Statistical Design Rationale

This allocation prioritizes **categorical signal validity** over traditional balanced design:

**Stadium Projects (Primary Focus):**
- Represent organizations optimizing under real constraint (high mutual information reducing entropy)
- Validate functor preservation: Does organizational structure → entropy reduction?
- Demonstrate adjoint relationship: Specification ⊣ Freedom duality observable in maintainer constraints
- Exhibit morphism abundance: High downloads = many composable interactions
- Expected effect size: Cohen's d > 0.8 (large)
- Statistical power: ~85% with α = 0.05

**Federation Projects (Theoretical Anchor):**
- Establish baseline organizational patterns
- Validate governance as natural category structure
- Full VSM system representation
- Expected effect size: Cohen's d ≈ 0.6 (medium)

**Club Projects (Convergence Case):**
- Validate low entropy → high coherence relationship
- Provide counterexample protection
- Informal but complete governance structures
- Expected effect size: Cohen's d ≈ 0.6 (medium)

**Control Group:**
- Estimate statistical noise
- Test null hypothesis
- Validate effect specificity

#### Power Analysis

```python
# Stadium-heavy design detectable effect sizes
stadium_n = 28
federation_n = 14
club_n = 10
control_n = 18

# Main effect (Stadium vs Federation comparison)
# With α = 0.05, power = 0.85
detectable_d = 0.50  # Medium effect size

# ANOVA across all groups
# With α = 0.05, power = 0.80
detectable_f = 0.35  # Medium effect size
```

**Key Advantage:** This design maximizes categorical coherence. Stadium projects form a natural subcategory where organizational functors (governance patterns, maintainer roles, review processes) most clearly map to entropy distribution changes. This provides **more valid inference**, not just more statistical power.

#### Information-Theoretic Justification

Using category theory and information theory, Stadium projects provide the cleanest signal:

**Mutual Information & Entropy Reduction:**
```
I(Organization; Entropy) = H(Entropy) - H(Entropy|Organization)
```

Stadium projects maximize this mutual information because:
1. **Constraint is real:** ≤3 maintainers = genuine organizational boundary
2. **Usage is validated:** High downloads = actual impact, not vanity metrics
3. **Composability is observable:** Many dependents = abundant morphisms
4. **Functorial preservation is testable:** Clear structure → outcome mappings

**Categorical Signal Properties:**

| Property | Stadium | Federation | Club | Control |
|----------|---------|------------|------|---------|
| **Morphism clarity** | High (few actors, clear roles) | Medium (complex structure) | Low (informal) | Variable |
| **Constraint observability** | High (maintainer count) | Medium (governance docs) | Low (implicit norms) | None |
| **Outcome measurement** | High (downloads, performance) | Medium (community metrics) | Low (niche metrics) | Variable |
| **Functorial testability** | High (clear mappings) | Medium (complex functors) | Low (emergent patterns) | Low |

**Expected Entropy Distributions:**

```python
# Hypothesized entropy by project type
stadium_entropy = Normal(μ=5.2, σ=1.1)      # Constrained but active
federation_entropy = Normal(μ=6.8, σ=1.4)   # High diversity, coordination cost
club_entropy = Normal(μ=4.1, σ=0.9)         # Low diversity, tight coherence
control_entropy = Normal(μ=6.0, σ=2.0)      # High variance, no structure

# Main effect detectable with Stadium-heavy design:
effect_size = (stadium_entropy.μ - federation_entropy.μ) / pooled_σ
# ≈ 1.28 (very large effect, easily detectable)
```

**The Stadium Advantage:** In category theory terms, Stadium projects are **terminal objects** in the organizational constraint category—they represent the limit of viable operation under minimal human resources. This makes them ideal for testing whether organizational structure (the functor) actually reduces entropy (the target category).

### Measurement Framework

**1. Project Classification (Asparouhova Quadrant)**
```python
user_growth = f(stars, forks, dependents, downloads)
contributor_growth = f(unique_authors, PR_authors, new_contributors)
quadrant = classify(user_growth, contributor_growth)
```

**2. VSM System Health (5 systems × 5-point scale)**
```python
S1_health = f(commit_frequency, PR_merge_rate, release_cadence)
S2_health = f(conflict_rate, review_turnaround, guideline_completeness)
S3_health = f(CI_coverage, test_coverage, metrics_availability)
S3star_health = f(audit_frequency, vulnerability_response, review_depth)
S4_health = f(dependency_freshness, roadmap_activity, ecosystem_engagement)
S5_health = f(governance_doc_clarity, mission_coherence, decision_consistency)
```

**3. Ostrom Principle Satisfaction (8 principles × 5-point scale)**
```python
for principle in ostrom_principles:
    score[principle] = evaluate(project, principle_rubric[principle])
```

**4. Entropy Indicators**
```python
H_config = entropy(code_style_distribution)
H_contrib = entropy(contribution_distribution)  
H_gov = entropy(decision_pattern_distribution)
H_temporal = entropy(activity_time_series)
```

**5. Outcome Variables**
```python
sustainability = f(longevity, activity_trend, maintainer_retention)
health = f(issue_resolution_rate, PR_acceptance_rate, release_stability)
community = f(contributor_growth, diversity_index, sentiment)
```

### Analysis Plan

**Phase 1: Stadium Entropy Profiling (PRIMARY)**
- Measure entropy distributions across Stadium sample (n=28-30)
- Calculate effect sizes: Stadium vs Federation, Stadium vs Club, Stadium vs Control
- Test H1: Stadium entropy structure differs significantly from other types
- Validate power analysis: Achieved power ≥ 0.85 for main effects

**Phase 2: Functorial Mapping (THEORETICAL)**
- Test categorical morphisms: governance operations → entropy distributions
- Measure morphism abundance: downloads, dependents, integrations
- Test H2: Functorial preservation in Stadium constraint conditions
- Validate Specification ⊣ Freedom adjunction observability

**Phase 3: Comparative Analysis (VALIDATION)**
- Federation baseline: Test Ostrom satisfaction ↔ viability (expected r > 0.6)
- Club convergence: Test low entropy ↔ high coherence
- Control noise: Establish baseline variance
- Test H3-H5: Differential framework applicability

**Phase 4: VSM Compression Analysis**
- Map VSM systems in Stadium vs Federation vs Club
- Test H4: VSM compression in constrained organizations
- Measure VSM → entropy functorial preservation
- Document compressed vs distributed governance structures

**Phase 5: Categorical Synthesis**
- Unify findings into categorical framework
- Formalize Stadium as terminal object in constraint category
- Document functorial semantics: Organization → Entropy → Outcomes
- Identify composition quality as viability predictor

#### Expected Statistical Outcomes

| Comparison | Expected Effect Size | Statistical Power | Significance |
|------------|---------------------|-------------------|--------------|
| **Stadium vs Federation entropy** | d > 0.8 (large) | 0.85 | p < 0.001 |
| **Stadium vs Club entropy** | d ≈ 0.9 (large) | 0.88 | p < 0.001 |
| **Stadium vs Control entropy** | d ≈ 0.6 (medium) | 0.75 | p < 0.01 |
| **Federation Ostrom correlation** | r > 0.6 | 0.80 | p < 0.01 |
| **Stadium Ostrom correlation** | r < 0.3 (NS) | — | p > 0.05 |
| **Overall ANOVA (4 groups)** | f ≈ 0.35-0.40 | 0.80 | p < 0.001 |

**Critical Tests:**
1. **Primary:** Stadium entropy significantly lower than Federation (validates constraint effect)
2. **Functorial:** Morphism abundance correlates with entropy reduction in Stadium (validates categorical semantics)
3. **Differential:** Ostrom predicts Federation but not Stadium viability (validates taxonomic distinction)
4. **Composition:** Morphism composition quality predicts outcomes in Stadium (validates categorical approach)

#### Design Comparison

```
TRADITIONAL BALANCED DESIGN (n=60)
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   Stadium    │  Federation  │     Club     │   Control    │
│    n=15      │    n=15      │    n=15      │    n=15      │
│   Power: 0.65│   Power: 0.65│   Power: 0.65│   Power: 0.65│
└──────────────┴──────────────┴──────────────┴──────────────┘
Detectable effect size: d ≥ 0.75 (medium-large)

STADIUM-OPTIMIZED DESIGN (n=70)
┌────────────────────────────────┬─────────────┬───────────┬──────────────┐
│          Stadium               │ Federation  │   Club    │   Control    │
│           n=28                 │   n=14      │   n=10    │    n=18      │
│         Power: 0.85            │ Power: 0.75 │Power: 0.70│ Power: 0.75  │
└────────────────────────────────┴─────────────┴───────────┴──────────────┘
Detectable effect size: d ≥ 0.50 (medium)

ADVANTAGE: +30% power for primary Stadium comparisons
           +33% efficiency in categorical signal detection
           Aligned with theoretical structure (Stadium as terminal object)
```

**Why This Matters:** The Stadium-optimized design doesn't just have more statistical power—it has **more valid inference**. By concentrating observations where the categorical structure is clearest (organizational constraint creates observable functorial mappings), we're more likely to detect real theoretical relationships rather than statistical noise.

---

## Getting Started

### Prerequisites

- **Python 3.10+** (3.11 or 3.12 recommended)
- **Git**
- **GitHub Personal Access Token** (for data collection)
  - Create at: https://github.com/settings/tokens
  - Required scopes: `public_repo`, `read:org`, `read:user`

### Installation

```bash
# Clone the repository
git clone https://github.com/ibrahimcesar/categories-of-the-commons.git
cd categories-of-the-commons

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your GitHub token
```

### Quick Start

**1. Verify installation:**
```bash
python -c "import src; print(src.__version__)"
```

**2. Test data collection:**
```bash
# Collect data for a Stadium project (e.g., curl)
python src/collection/github_collector.py
```

**3. Calculate entropy:**
```bash
# Run entropy calculation example
python src/analysis/entropy_calculation.py
```

**4. Explore with Jupyter:**
```bash
jupyter lab
# Open notebooks/01_data_exploration.ipynb
```

### Project Structure

Review [data/projects.json](data/projects.json) to see the Stadium-optimized sample design and add project nominations.

### Development

**Run tests:**
```bash
pytest
```

**Check code style:**
```bash
black src/
flake8 src/
mypy src/
```

**Generate documentation:**
```bash
cd docs/
sphinx-build -b html . _build/
```

### Data Collection Workflow

1. **Identify projects** → Update `data/projects.json`
2. **Collect metrics** → Run `github_collector.py`
3. **Calculate entropy** → Run `entropy_calculation.py`
4. **Analyze** → Use Jupyter notebooks in `notebooks/`
5. **Visualize** → Generate figures in `results/figures/`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

---

## Repository Structure

```
categories-of-the-commons/
│
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
│
├── paper/                       # Academic paper
│   ├── main.tex                 # LaTeX source
│   ├── references.bib           # Bibliography
│   ├── figures/                 # Generated figures
│   └── sections/                # Paper sections
│
├── theory/                      # Theoretical framework
│   ├── sheaf-cohomology-framework.md  # Sheaf theory & Čech cohomology
│   ├── categorical-foundations.md
│   ├── vsm-oss-mapping.md
│   ├── ostrom-formalization.md
│   └── entropy-framework.md
│
├── data/                        # Data collection
│   ├── raw/                     # Raw API responses
│   ├── processed/               # Cleaned datasets
│   ├── projects.json            # Project sample list
│   └── classification/          # Quadrant classifications
│
├── src/                         # Analysis code
│   ├── collection/              # Data collection scripts
│   │   ├── github_collector.py
│   │   ├── metrics_collector.py
│   │   └── governance_parser.py
│   ├── analysis/                # Analysis modules
│   │   ├── vsm_health.py
│   │   ├── ostrom_scoring.py
│   │   ├── entropy_calculation.py
│   │   └── categorical_analysis.py
│   ├── visualization/           # Plotting
│   └── utils/                   # Helpers
│
├── notebooks/                   # Jupyter notebooks
│   ├── 00_setup_and_test.ipynb
│   ├── 01_data_exploration.ipynb
│   ├── 02_batch_collection.ipynb
│   ├── 03_statistical_analysis.ipynb
│   ├── 04_category_theory.ipynb
│   ├── 05_vsm_mapping.ipynb
│   ├── 06_temporal_analysis.ipynb
│   ├── 07_visualization_report.ipynb
│   └── 08_sheaf_cohomology.ipynb   # Governance cohomology analysis
│
├── results/                     # Output
│   ├── tables/                  # Statistical tables
│   ├── figures/                 # Visualizations
│   └── reports/                 # Generated reports
│
├── interviews/                  # Optional qualitative data
│   ├── protocol.md              # Interview protocol
│   ├── consent.md               # Consent form
│   └── transcripts/             # Anonymized transcripts
│
└── docs/                        # Documentation
    ├── methodology.md           # Detailed methodology
    ├── codebook.md              # Variable definitions
    └── replication.md           # Replication guide
```

---

## Key Hypotheses

### H1: Stadium Entropy Structure (PRIMARY)
*Stadium projects exhibit distinct entropy profiles due to organizational constraint.*

- **H1a:** Stadium entropy (μ ≈ 5.2) differs significantly from Federation entropy (μ ≈ 6.8) with large effect size (d > 0.8)
- **H1b:** Stadium entropy variance (σ ≈ 1.1) is lower than control variance, indicating structural constraint
- **H1c:** Stadium projects with performance data show stronger organization → entropy reduction mapping (higher mutual information)
- **H1d:** Maintainer count constraint (≤3) creates observable categorical terminal object structure

### H2: Functorial Preservation (THEORETICAL)
*Organizational functors preserve compositional structure in Stadium projects.*

- **H2a:** Stadium governance patterns (review processes, merge operations) map functorially to entropy distributions
- **H2b:** Morphism abundance (download count, dependent projects) correlates with entropy reduction efficiency
- **H2c:** Specification ⊣ Freedom adjunction is observable in Stadium constraint dynamics
- **H2d:** Federation projects show functorial preservation but with higher complexity (medium effect size, d ≈ 0.6)

### H3: Entropy as Categorical Indicator
*Entropy serves as the key observable in the categorical semantics.*

- **H3a:** Stadium projects demonstrate clearest entropy → outcome relationship (highest signal-to-noise)
- **H3b:** Club projects validate low entropy → high coherence (convergent case)
- **H3c:** Federation projects show governance structure → entropy modulation (baseline case)
- **H3d:** Control group shows higher entropy variance, validating structural effects in other groups

### H4: VSM Compression in Stadiums
*Stadium VSM systems collapse onto minimal maintainer set.*

- **H4a:** Stadium VSM shows "compressed" structure (all 5 systems present but embodied in ≤3 people)
- **H4b:** VSM compression correlates with entropy profiles (compressed VSM → constrained entropy)
- **H4c:** Federation VSM shows distributed structure (systems across multiple organizational units)
- **H4d:** VSM structure → entropy mapping is functorial (preserves composition)

### H5: Ostrom Inapplicability to Stadiums
*Ostrom's framework applies differentially, validating taxonomic distinctions.*

- **H5a:** Stadium viability does NOT correlate with Ostrom principle satisfaction (r < 0.3)
- **H5b:** Federation viability correlates strongly with Ostrom satisfaction (r > 0.6, medium effect)
- **H5c:** Club viability correlates moderately with Ostrom satisfaction (r ≈ 0.4-0.5)
- **H5d:** Stadium viability correlates instead with: employer backing, funding, succession planning, automation

### H6: Categorical Composition Quality
*Morphism composition quality predicts outcomes, observable primarily in Stadium projects.*

- **H6a:** Stadium projects where governance morphisms compose cleanly (low composition failure rate) have better sustainability
- **H6b:** Composition failures (blocked PRs, unresolved conflicts) predict decline more strongly in Stadiums than Federations
- **H6c:** Morphism abundance (dependencies, integrations) without composition quality leads to entropy increase
- **H6d:** The Governance ⊣ Freedom adjunction balance is most observable in Stadium constraint conditions

---

## Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| **1. Foundation** | Month 1-2 | Literature review, framework formalization, methodology refinement |
| **2. Data Collection** | Month 2-4 | API data extraction, governance document analysis, classification |
| **3. Quantitative Analysis** | Month 4-6 | VSM scoring, Ostrom evaluation, entropy calculation, statistical analysis |
| **4. Qualitative Enrichment** | Month 5-7 | Optional maintainer interviews, case studies |
| **5. Synthesis** | Month 7-8 | Framework refinement, theoretical contribution articulation |
| **6. Writing** | Month 8-10 | Paper drafting, revision, submission |

---

## Contributing

This is independent academic research, but contributions are welcome:

- **Theoretical feedback:** Critiques of the categorical framework
- **Methodology suggestions:** Improvements to measurement approaches
- **Project nominations:** OSS projects that would test the framework well
- **Data validation:** Verification of classifications and scores
- **Replication:** Independent replication attempts

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Related Work

### Foundational Texts

**Cybernetics & VSM:**
- Beer, S. (1972). *Brain of the Firm*. Allen Lane.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley & Sons.
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley & Sons.

**Commons Governance:**
- Ostrom, E. (1990). *Governing the Commons*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.

**Open Source:**
- Asparouhova, N. (2020). *Working in Public: The Making and Maintenance of Open Source Software*. Stripe Press.
- Raymond, E. S. (1999). *The Cathedral and the Bazaar*. O'Reilly Media.
- Schweik, C. M., & English, R. C. (2012). *Internet Success: A Study of Open-Source Software Commons*. MIT Press.

**Category Theory:**
- Mac Lane, S. (1998). *Categories for the Working Mathematician* (2nd ed.). Springer.
- Fong, B., & Spivak, D. I. (2019). *An Invitation to Applied Category Theory*. Cambridge University Press.
- Riehl, E. (2016). *Category Theory in Context*. Dover Publications.

### Key Papers

**OSS Governance:**
- Fogel, K. (2005). *Producing Open Source Software*. O'Reilly Media.
- O'Mahony, S., & Ferraro, F. (2007). The emergence of governance in an open source community. *Academy of Management Journal*, 50(5), 1079-1106.

**Sustainability:**
- Eghbal, N. (2016). *Roads and Bridges: The Unseen Labor Behind Our Digital Infrastructure*. Ford Foundation.
- Coelho, J., & Valente, M. T. (2017). Why modern open source projects fail. *FSE 2017*.

**Metrics:**
- CHAOSS Project. Community Health Analytics Open Source Software.
- OpenSSF Scorecard. Security health metrics for open source projects.

---

## Author

**Ibrahim Cesar**  
Independent Researcher  
São Paulo, Brazil

- **Email:** ibrahim@ibrahimcesar.com
- **Web:** https://ibrahimcesar.com
- **ORCID:** [0009-0006-9954-659X](https://orcid.org/0009-0006-9954-659X)
- **Google Scholar:** [cf_7W3cAAAAJ](https://scholar.google.com/citations?user=cf_7W3cAAAAJ)

**Affiliation:**  
MBA in Strategic Management of Operations, Projects and IT  
University of São Paulo (USP) | EACH

---

## Disclaimer

⚠️ **This is independent academic research.**

This work is not affiliated with, sponsored by, or representative of any employer or commercial entity. The research, methodology, findings, and any publications are entirely my own.

---

## Citation

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

---

## License

This work is licensed under the [MIT License](LICENSE).

The theoretical framework, methodology, and analysis code are open for academic use. Please cite appropriately.

---

## Acknowledgments

This research builds upon the intellectual foundations laid by:

- **Stafford Beer** — for showing that organizations are viable systems
- **Elinor Ostrom** — for proving that commons can be governed successfully
- **Nadia Asparouhova** — for seeing open source as it actually is
- **Saunders Mac Lane & Samuel Eilenberg** — for creating the language of composition

And to the countless open source maintainers who make the digital commons possible.

---

## Appendix: VSM Health Badges for Projects

This research includes a public API that generates VSM Health badges for any GitHub repository. Project maintainers can embed these badges in their READMEs.

**API Base URL:** `https://categories-of-the-commons-omg5alawo-ibrahim-cesars-projects.vercel.app`

**Quick Start:**
```markdown
![VSM Health](https://categories-of-the-commons-omg5alawo-ibrahim-cesars-projects.vercel.app/badge/YOUR_ORG/YOUR_REPO)
```

**Available Endpoints:**

| Endpoint | Returns |
|----------|---------|
| `/badge/{owner}/{repo}` | Simple shields-style badge |
| `/card/{owner}/{repo}?theme=dark\|light` | Detailed card with S1-S5 breakdown |
| `/mini/{owner}/{repo}?theme=dark\|light` | Compact card with radar chart |
| `/report/{owner}/{repo}` | JSON health report |

**Improve Your Score:** Add governance files (`GOVERNANCE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, `ROADMAP.md`) and enable GitHub Discussions.

**Self-Hosted:** Use `scripts/generate_vsm_badge.py` or the GitHub Action in `templates/workflows/update-vsm-badge.yml`.

---

<div align="center">

*"In the beginning was the morphism."*

**Categories of the Commons** | 2025

</div>
