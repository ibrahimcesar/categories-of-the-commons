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

We operationalize this framework through **entropy measurement** on publicly available OSS data, testing whether categorical structure predicts project viability across different governance models.

**Keywords:** Open Source Software, Commons Governance, Category Theory, Cybernetics, Viable System Model, Institutional Analysis, Organizational Entropy

---

## Table of Contents

- [Research Questions](#research-questions)
- [Theoretical Framework](#theoretical-framework)
  - [The Four Project Types](#the-four-project-types)
  - [Viable System Model for OSS](#viable-system-model-for-oss)
  - [Ostrom's Design Principles](#ostroms-design-principles)
  - [Categorical Formalization](#categorical-formalization)
  - [Entropy as Viability Indicator](#entropy-as-viability-indicator)
- [Methodology](#methodology)
- [Repository Structure](#repository-structure)
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
│                    ENVIRONMENT                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 SYSTEM 5: POLICY                      │  │
│  │     Identity, Values, Strategic Direction             │  │
│  │     [GOVERNANCE.md, Mission, Core Values]             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               SYSTEM 4: INTELLIGENCE                  │  │
│  │     Environmental Scanning, Future Planning           │  │
│  │     [Roadmaps, RFCs, Ecosystem Monitoring]            │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │     SYSTEM 3: CONTROL    │    SYSTEM 3*: AUDIT       │  │
│  │     Operational Oversight │    Direct Verification    │  │
│  │     [Metrics, Releases]   │    [Security Audits]      │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │               SYSTEM 2: COORDINATION                  │  │
│  │     Conflict Resolution, Standards, Anti-oscillation  │  │
│  │     [CONTRIBUTING.md, CI/CD, Code Review]             │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↕                                  │
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

Stratified sampling across Asparouhova's taxonomy:

| Quadrant | Sample | Selection Criteria | Comparison |
|----------|--------|-------------------|------------|
| Federation | 15 | CNCF/Apache/LF projects | 8 healthy, 7 struggling |
| Stadium | 20 | High downloads, ≤3 maintainers | 10 healthy, 10 struggling |
| Club | 15 | Active niche communities | 8 healthy, 7 struggling |
| Toy | 10 | Control group | Random sample |

**Total: 60 projects**

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

**Phase 1: Descriptive**
- Characterize each quadrant's typical categorical structure
- Map VSM system presence/absence by project type
- Document Ostrom principle satisfaction patterns

**Phase 2: Correlational**
- VSM health ↔ sustainability outcomes
- Ostrom satisfaction ↔ governance effectiveness
- Entropy levels ↔ project health
- Categorical properties ↔ viability

**Phase 3: Predictive**
- Can entropy trajectories predict governance crises?
- Do categorical composition failures precede project decline?
- What early indicators distinguish sustainable from failing projects?

**Phase 4: Theoretical**
- Synthesize findings into unified categorical framework
- Identify quadrant-specific viability conditions
- Formalize the Stadium problem and potential solutions

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
│   ├── 01_data_exploration.ipynb
│   ├── 02_quadrant_classification.ipynb
│   ├── 03_vsm_analysis.ipynb
│   ├── 04_ostrom_analysis.ipynb
│   ├── 05_entropy_analysis.ipynb
│   └── 06_synthesis.ipynb
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

### H1: Taxonomic Differentiation
*Different project types exhibit systematically different governance structures.*

- **H1a:** Federations have the richest categorical structure (most morphism types, complex composition)
- **H1b:** Stadiums have collapsed VSM (all systems in one person)
- **H1c:** Clubs have informal but complete VSM
- **H1d:** Categorical structure complexity correlates with governance formalization

### H2: Ostrom Selectivity
*Ostrom's principles predict viability differentially by project type.*

- **H2a:** Federation viability correlates strongly with Ostrom principle satisfaction (r > 0.6)
- **H2b:** Stadium viability does not correlate with Ostrom satisfaction (collective action framework doesn't apply)
- **H2c:** Stadium viability correlates with maintainer support factors (funding, employer backing, succession planning)
- **H2d:** Club viability correlates moderately with Ostrom satisfaction

### H3: VSM Universality
*VSM system health predicts viability across all project types.*

- **H3a:** Projects with all five VSM systems represented are more sustainable
- **H3b:** System 2 (Coordination) deficiency predicts governance crises
- **H3c:** System 4 (Intelligence) deficiency predicts technological obsolescence
- **H3d:** System 5 (Policy) deficiency predicts community fragmentation

### H4: Entropy Dynamics
*Entropy trajectories provide early warning of viability threats.*

- **H4a:** Rapidly increasing entropy precedes governance crises
- **H4b:** Persistently low entropy precedes maintainer burnout (Stadium) or stagnation (Club)
- **H4c:** Healthy projects exhibit entropy oscillation (breathing pattern)
- **H4d:** Entropy normalization (return to moderate levels) follows successful governance interventions

### H5: Categorical Prediction
*Categorical composition quality predicts outcomes across all types.*

- **H5a:** Projects where governance morphisms compose cleanly have better outcomes
- **H5b:** Composition failures (blocked PRs, unresolved conflicts, decision deadlocks) predict decline
- **H5c:** The Governance ⊣ Freedom adjunction balance correlates with sustainability

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

<div align="center">

*"In the beginning was the morphism."*

**Categories of the Commons** | 2025

</div>
