# Research Project TODO

This document tracks all tasks for the Categories of the Commons research project, organized by phase and priority.

**Legend:**
- 🔴 Critical path / High priority
- 🟡 Important / Medium priority
- 🟢 Nice to have / Low priority
- ✅ Completed
- 🚧 In progress
- ⏸️ Blocked / Waiting
- 📅 Future / Backlog

---

## Phase 1: Project Identification & Classification (Weeks 1-3)

### 🔴 Stadium Projects (Target: 28-30)

**Identification Criteria:**
- High downloads: >100k/month (npm), >1M total (PyPI), >10M downloads (crates.io)
- ≤3 core maintainers
- Active: commits in last 6 months
- Performance data available
- Real organizational impact

#### JavaScript/Node.js
- [ ] curl-like HTTP clients (axios, node-fetch, got)
- [ ] core-js (polyfills) - **Known burnout case**
- [ ] Babel plugins ecosystem
- [ ] eslint-config-* packages
- [ ] Popular CLI tools (chalk, commander, yargs)
- [ ] Utility libraries (lodash maintainers, date-fns)

#### Python
- [ ] requests - **Classic Stadium**
- [ ] click (CLI framework)
- [ ] python-dateutil
- [ ] six (Python 2/3 compatibility)
- [ ] Popular pip packages with few maintainers

#### Rust
- [ ] serde ecosystem packages
- [ ] tokio components
- [ ] clap (CLI parser)
- [ ] regex crate

#### Other Languages
- [ ] curl (C) - **Iconic Stadium project**
- [ ] SQLite (C) - Single maintainer, massive usage
- [ ] ImageMagick components
- [ ] nginx modules

**Actions:**
- [ ] 🔴 Create spreadsheet for candidate projects
- [ ] 🔴 Verify maintainer count via GitHub API
- [ ] 🔴 Verify download metrics via package registries
- [ ] 🔴 Document rationale for each selection
- [ ] 🟡 Identify 5 "healthy" vs 5 "struggling" for comparison

### 🟡 Federation Projects (Target: 12-15)

**Identification Criteria:**
- CNCF/Apache/Linux Foundation backing preferred
- Documented governance (GOVERNANCE.md, RFCs, SIGs)
- High contributor and user growth
- Multi-stakeholder decision-making

#### Confirmed Candidates
- [ ] Kubernetes (CNCF) - SIGs, extensive governance
- [ ] Rust (Rust Foundation) - RFC process, teams
- [ ] Python (PSF) - PEPs, steering council
- [ ] Node.js (OpenJS) - Technical Steering Committee
- [ ] Linux Kernel - Hierarchical maintainership
- [ ] Apache projects (Kafka, Cassandra, Spark)
- [ ] CNCF projects (Prometheus, Envoy, Helm)

**Actions:**
- [ ] 🔴 Select 12-15 projects with varying governance models
- [ ] 🔴 Collect governance documentation URLs
- [ ] 🟡 Map governance structures to Ostrom principles
- [ ] 🟡 Identify crisis/transition events for longitudinal analysis

### 🟡 Club Projects (Target: 8-10)

**Identification Criteria:**
- Niche domain/community
- High contributor-to-user ratio
- Tight community cohesion (Discord/Slack/forum activity)
- Specialized technical focus

#### Candidate Domains
- [ ] Academic/research software (scientific Python, bioinformatics)
- [ ] Domain-specific frameworks (game dev, embedded, specialized ML)
- [ ] Language-specific tooling communities
- [ ] Niche web frameworks
- [ ] Specialized database adapters

**Actions:**
- [ ] 🟡 Identify 8-10 club projects across different domains
- [ ] 🟡 Verify community activity (Discord/forum metrics)
- [ ] 🟡 Document community cohesion indicators

### 🟢 Control Group (Target: 15-20)

**Actions:**
- [ ] 🟢 Random sampling methodology (stratified by language/domain)
- [ ] 🟢 Ensure mix of project types and sizes
- [ ] 🟢 Establish baseline variance

---

## Phase 2: Data Collection Infrastructure (Weeks 2-4)

### 🔴 GitHub API Collection

#### Core Metrics
- [x] ✅ Basic repository metrics (stars, forks, watchers)
- [x] ✅ Contributor data collection
- [x] ✅ Commit history extraction
- [x] ✅ Governance file detection
- [ ] 🔴 Pull request data (merge rate, review turnaround, conflict rate)
- [ ] 🔴 Issue data (resolution rate, types, sentiment)
- [ ] 🔴 Release data (cadence, version patterns)
- [ ] 🟡 GitHub Discussions/Forum activity
- [ ] 🟡 Dependency information (dependents, dependencies)
- [ ] 🟡 CI/CD configuration detection

#### Advanced Collection
- [ ] 🟡 PR review patterns (approvers, comment patterns)
- [ ] 🟡 Maintainer identification heuristics
- [ ] 🟡 Code ownership patterns (CODEOWNERS, commit patterns)
- [ ] 🟡 Branch protection rules
- [ ] 🟢 Security policy detection
- [ ] 🟢 Sponsorship/funding information

**Actions:**
- [ ] 🔴 Extend github_collector.py with PR/issue methods
- [ ] 🔴 Implement rate limiting and caching
- [ ] 🔴 Add error handling and retry logic
- [ ] 🟡 Create data validation checks
- [ ] 🟡 Build incremental update capability

### 🔴 Package Registry APIs

#### npm (JavaScript)
- [ ] 🔴 Download statistics
- [ ] 🔴 Dependent count
- [ ] 🟡 Version history

#### PyPI (Python)
- [ ] 🔴 Download statistics (pypistats)
- [ ] 🔴 Project metadata
- [ ] 🟡 Package health indicators

#### crates.io (Rust)
- [ ] 🔴 Download metrics
- [ ] 🔴 Dependency graph

#### Others
- [ ] 🟡 Maven Central (Java)
- [ ] 🟡 RubyGems
- [ ] 🟢 NuGet (.NET)

**Actions:**
- [ ] 🔴 Create package_metrics_collector.py
- [ ] 🔴 Implement registry-specific APIs
- [ ] 🟡 Normalize metrics across registries

### 🟡 Governance Document Parsing

- [ ] 🔴 Extract GOVERNANCE.md content
- [ ] 🔴 Parse CONTRIBUTING.md guidelines
- [ ] 🔴 Detect CODE_OF_CONDUCT presence
- [ ] 🟡 Extract maintainer lists (MAINTAINERS.md, CODEOWNERS)
- [ ] 🟡 Parse RFC/PEP/proposal processes
- [ ] 🟡 NLP analysis of governance text
- [ ] 🟢 Sentiment analysis of governance docs

**Actions:**
- [ ] 🔴 Create governance_parser.py
- [ ] 🟡 Build structured extraction pipeline
- [ ] 🟡 Create governance document database

### 🟢 External Data Sources

- [ ] 🟡 OpenSSF Scorecard metrics
- [ ] 🟡 CHAOSS metrics (if available)
- [ ] 🟡 Libraries.io data
- [ ] 🟢 Stack Overflow mention frequency
- [ ] 🟢 Twitter/social media mentions
- [ ] 🟢 Job posting mentions (tech stack popularity)

---

## Phase 3: Analysis Implementation (Weeks 4-6)

### 🔴 Entropy Calculations

#### Implementation
- [x] ✅ Shannon entropy base implementation
- [x] ✅ Contributor entropy
- [x] ✅ Temporal entropy (commit patterns)
- [x] ✅ File change entropy
- [ ] 🔴 Governance entropy (decision pattern consistency)
- [ ] 🔴 Communication entropy (issue/PR discussion patterns)
- [ ] 🟡 Code style entropy (linting violations, patterns)
- [ ] 🟡 Dependency entropy (change frequency)

#### Validation
- [x] ✅ Unit tests for entropy calculations
- [ ] 🔴 Validate against known cases (high/low entropy projects)
- [ ] 🟡 Cross-validate with expert assessments
- [ ] 🟡 Test entropy normalization methods

**Actions:**
- [ ] 🔴 Extend entropy_calculation.py with new measures
- [ ] 🔴 Create entropy aggregation method
- [ ] 🔴 Build entropy time-series analysis
- [ ] 🟡 Implement entropy "breathing" pattern detection

### 🔴 VSM System Health Scoring

- [ ] 🔴 Create vsm_health.py module
- [ ] 🔴 Define S1 (Operations) indicators:
  - Commit frequency, PR merge rate, release cadence
- [ ] 🔴 Define S2 (Coordination) indicators:
  - PR conflict rate, review turnaround, guideline completeness
- [ ] 🔴 Define S3 (Control) indicators:
  - CI/CD coverage, test coverage, metrics availability
- [ ] 🔴 Define S3* (Audit) indicators:
  - Security audits, vulnerability response, review depth
- [ ] 🔴 Define S4 (Intelligence) indicators:
  - Dependency updates, roadmap activity, ecosystem engagement
- [ ] 🔴 Define S5 (Policy) indicators:
  - Governance clarity, mission coherence, decision consistency
- [ ] 🟡 Create 5-point scoring rubric for each system
- [ ] 🟡 Implement automated scoring where possible
- [ ] 🟡 Build VSM visualization (diagrams)

### 🔴 Ostrom Principle Evaluation

- [ ] 🔴 Create ostrom_scoring.py module
- [ ] 🔴 Define scoring rubric for 8 principles:
  1. Clearly defined boundaries
  2. Congruence
  3. Collective-choice arrangements
  4. Monitoring
  5. Graduated sanctions
  6. Conflict resolution mechanisms
  7. Recognition of rights to organize
  8. Nested enterprises
- [ ] 🟡 Map GitHub features to principles
- [ ] 🟡 Implement automated scoring where possible
- [ ] 🟡 Create principle satisfaction matrix

### 🟡 Categorical Analysis

- [ ] 🔴 Create categorical_analysis.py module
- [ ] 🔴 Define morphism identification:
  - Contribution flows (commits, PRs)
  - Review relationships (reviewer graphs)
  - Merge operations (composition patterns)
  - Governance decisions (policy changes)
- [ ] 🔴 Implement morphism counting and classification
- [ ] 🟡 Detect composition failures:
  - Blocked PRs
  - Unresolved conflicts
  - Decision deadlocks
- [ ] 🟡 Measure morphism abundance (dependencies, integrations)
- [ ] 🟡 Analyze functorial preservation (structure → outcome mappings)
- [ ] 🟢 Implement category visualization (networkx graphs)

### 🟡 Statistical Analysis

- [ ] 🔴 Implement effect size calculations (Cohen's d, r)
- [ ] 🔴 Build ANOVA for 4-group comparison
- [ ] 🔴 Create correlation matrices
- [ ] 🔴 Implement power analysis validation
- [ ] 🟡 Build regression models (entropy → outcomes)
- [ ] 🟡 Implement time-series analysis for trajectories
- [ ] 🟡 Create survival analysis for project longevity
- [ ] 🟢 Build machine learning predictive models

---

## Phase 4: Jupyter Notebooks & EDA (Weeks 5-7)

### 🔴 Core Notebooks

- [ ] 🔴 **01_data_exploration.ipynb**
  - Data loading and validation
  - Descriptive statistics
  - Missing data analysis
  - Distribution visualizations

- [ ] 🔴 **02_quadrant_classification.ipynb**
  - Classify projects into Stadium/Federation/Club/Control
  - Visualize quadrant boundaries
  - Validate classification criteria

- [ ] 🔴 **03_entropy_analysis.ipynb**
  - Calculate all entropy measures
  - Compare entropy distributions by quadrant
  - Test H1: Stadium entropy structure
  - Visualize entropy distributions

- [ ] 🔴 **04_stadium_focus.ipynb** (PRIMARY)
  - Deep dive into Stadium projects
  - Stadium vs Federation comparison (main effect)
  - Stadium vs Club comparison
  - Stadium vs Control comparison
  - Effect size calculations
  - Power analysis validation

- [ ] 🟡 **05_vsm_analysis.ipynb**
  - VSM system health by project type
  - VSM compression in Stadiums
  - VSM → entropy correlation
  - Test H4: VSM compression

- [ ] 🟡 **06_ostrom_analysis.ipynb**
  - Ostrom principle satisfaction by type
  - Test H5: Differential applicability
  - Federation correlation analysis
  - Stadium non-correlation validation

- [ ] 🟡 **07_categorical_analysis.ipynb**
  - Morphism identification and counting
  - Functorial preservation tests
  - Composition quality analysis
  - Test H2 & H6: Categorical structure

- [ ] 🔴 **08_statistical_tests.ipynb**
  - Primary hypothesis tests
  - Effect size calculations
  - Power analysis
  - Multiple comparison corrections
  - Confidence intervals

- [ ] 🟡 **09_visualizations.ipynb**
  - Publication-quality figures
  - Entropy distribution plots
  - VSM radar charts
  - Categorical structure diagrams
  - Effect size forest plots

- [ ] 🟡 **10_synthesis.ipynb**
  - Synthesize all findings
  - Answer research questions
  - Validate hypotheses
  - Identify unexpected patterns
  - Future research directions

---

## Phase 5: Visualization & Figures (Weeks 6-8)

### 🔴 Core Visualizations

- [ ] 🔴 Entropy distribution by project type (violin plots)
- [ ] 🔴 Stadium vs Federation comparison (box plots, effect size)
- [ ] 🔴 Power analysis validation chart
- [ ] 🔴 Sample allocation comparison (traditional vs optimized)
- [ ] 🟡 VSM system health radar charts
- [ ] 🟡 Ostrom principle satisfaction heatmap
- [ ] 🟡 Morphism abundance vs entropy scatter plot
- [ ] 🟡 Categorical structure network diagrams
- [ ] 🟡 Entropy time-series (breathing patterns)
- [ ] 🟢 Interactive visualizations (Plotly dashboards)

**Actions:**
- [ ] 🔴 Create visualization/ module with plotting utilities
- [ ] 🔴 Establish consistent style guide (colors, fonts)
- [ ] 🟡 Generate high-resolution figures for paper
- [ ] 🟡 Create supplementary material figures

---

## Phase 6: Paper Writing (Weeks 7-10)

### 🔴 LaTeX Structure

- [ ] 🔴 Set up paper/main.tex
- [ ] 🔴 Create paper/references.bib
- [ ] 🔴 Set up sections:
  - [ ] Abstract
  - [ ] Introduction
  - [ ] Related Work
  - [ ] Theoretical Framework
  - [ ] Methodology
  - [ ] Results
  - [ ] Discussion
  - [ ] Limitations
  - [ ] Conclusion
  - [ ] Future Work

### 🔴 Content Development

- [ ] 🔴 Write Abstract (200-250 words)
- [ ] 🔴 Write Introduction
  - Problem statement
  - Research questions
  - Contributions
- [ ] 🟡 Write Related Work
  - OSS governance literature
  - Cybernetics and VSM
  - Ostrom and commons
  - Category theory applications
- [ ] 🔴 Write Theoretical Framework
  - Asparouhova taxonomy
  - VSM for OSS
  - Ostrom principles
  - Categorical formalization
  - Entropy framework
- [ ] 🔴 Write Methodology
  - Stadium-optimized design rationale
  - Sample selection criteria
  - Data collection procedures
  - Measurement framework
  - Statistical analysis plan
- [ ] 🔴 Write Results
  - Descriptive statistics
  - Hypothesis test results
  - Effect sizes and power
  - Primary findings (Stadium focus)
  - Secondary findings
- [ ] 🔴 Write Discussion
  - Interpret findings
  - Stadium as terminal object
  - Functorial preservation
  - Ostrom inapplicability
  - Theoretical implications
- [ ] 🟡 Write Limitations
  - Sample limitations
  - Measurement challenges
  - Generalizability
- [ ] 🔴 Write Conclusion
  - Summary of contributions
  - Practical implications
  - Future research

### 🟡 Supplementary Materials

- [ ] 🟡 Appendix A: Project sample list
- [ ] 🟡 Appendix B: Measurement rubrics
- [ ] 🟡 Appendix C: Statistical details
- [ ] 🟡 Appendix D: Additional figures
- [ ] 🟢 Online repository with full data and code

---

## Phase 7: Optional Qualitative Enrichment (Weeks 5-9)

### 🟢 Maintainer Interviews

- [ ] 🟢 Finalize interview protocol (interviews/protocol.md)
- [ ] 🟢 Create consent form (interviews/consent.md)
- [ ] 🟢 Identify interview candidates (5-10 Stadium, 3-5 Federation)
- [ ] 🟢 Conduct interviews
- [ ] 🟢 Transcribe and anonymize
- [ ] 🟢 Thematic analysis
- [ ] 🟢 Integrate qualitative findings

---

## Infrastructure & Development (Ongoing)

### 🟡 Testing & Quality

- [x] ✅ Initial pytest setup
- [x] ✅ Entropy calculation tests
- [ ] 🟡 Data collector tests
- [ ] 🟡 VSM scoring tests
- [ ] 🟡 Integration tests
- [ ] 🟡 Achieve >80% test coverage
- [ ] 🟢 Set up CI/CD (GitHub Actions)

### 🟡 Documentation

- [x] ✅ README.md with research design
- [x] ✅ CONTRIBUTING.md
- [x] ✅ QUICK_START.md
- [ ] 🟡 API documentation (Sphinx)
- [ ] 🟡 Code examples and tutorials
- [ ] 🟡 Replication guide (docs/replication.md)
- [ ] 🟢 Video tutorial/walkthrough

### 🟢 Code Quality

- [ ] 🟡 Consistent docstrings (Google style)
- [ ] 🟡 Type hints throughout
- [ ] 🟡 Black formatting enforced
- [ ] 🟡 Flake8 passing
- [ ] 🟡 MyPy type checking
- [ ] 🟢 Pre-commit hooks

### 🟢 Performance

- [ ] 🟢 Optimize data collection (parallel requests)
- [ ] 🟢 Cache API responses
- [ ] 🟢 Optimize entropy calculations (vectorization)
- [ ] 🟢 Profile slow operations

---

## Publication & Dissemination (Weeks 10-12)

### 🔴 Paper Submission

- [ ] 🔴 Identify target venues:
  - [ ] FSE (Foundations of Software Engineering)
  - [ ] ICSE (International Conference on Software Engineering)
  - [ ] MSR (Mining Software Repositories)
  - [ ] CSCW (Computer-Supported Cooperative Work)
  - [ ] OSS (Open Source Systems)
- [ ] 🔴 Format paper to venue requirements
- [ ] 🔴 Prepare submission materials
- [ ] 🔴 Submit paper

### 🟡 Preprint & Code Release

- [ ] 🟡 Submit to arXiv
- [ ] 🟡 Release code and data on GitHub
- [ ] 🟡 Create Zenodo DOI
- [ ] 🟡 Prepare replication package

### 🟢 Community Engagement

- [ ] 🟢 Blog post summarizing findings
- [ ] 🟢 Twitter thread with key insights
- [ ] 🟢 Present at local meetups
- [ ] 🟢 Submit to practitioner conferences (FOSDEM, etc.)

---

## Current Sprint (Next 2 Weeks)

### Week 1 Priority
1. ✅ Complete project setup
2. **🔴 Identify 10 Stadium projects** (start with curl, core-js, requests)
3. **🔴 Extend github_collector.py** with PR/issue data
4. **🔴 Create package_metrics_collector.py**
5. **🟡 Start 01_data_exploration.ipynb**

### Week 2 Priority
1. **🔴 Collect data for first 10 Stadium projects**
2. **🔴 Complete entropy calculations for initial sample**
3. **🔴 Create vsm_health.py module**
4. **🔴 Start 03_entropy_analysis.ipynb**
5. **🟡 Identify 5 Federation projects**

---

## Notes & Decisions

### Design Decisions
- Stadium-optimized design: 28-30 Stadium, 12-15 Federation, 8-10 Club, 15-20 Control
- Target statistical power: 85% for d ≥ 0.50
- Primary comparison: Stadium vs Federation entropy
- Information-theoretic justification: Maximize I(Organization; Entropy)

### Open Questions
- [ ] Should we include Toy projects or merge into Control?
- [ ] What's the right time window for "active" projects? (6 months? 12 months?)
- [ ] How to handle projects transitioning between quadrants?
- [ ] Should we track projects longitudinally or point-in-time?
- [ ] What's the minimum download threshold for Stadium projects?

### Risks & Mitigations
- **Risk:** GitHub API rate limits
  - **Mitigation:** Caching, incremental updates, multiple tokens
- **Risk:** Hard to find true Club projects
  - **Mitigation:** Expand search to academic/niche domains
- **Risk:** Governance documents incomplete
  - **Mitigation:** Supplement with maintainer interviews
- **Risk:** Effect sizes smaller than expected
  - **Mitigation:** Stadium-heavy design gives 85% power for d=0.50

---

## Long-term Future Work

- [ ] 📅 Longitudinal study (track projects over time)
- [ ] 📅 Expand to GitLab, Bitbucket, self-hosted repos
- [ ] 📅 Build predictive models for project sustainability
- [ ] 📅 Create practitioner tool for project health assessment
- [ ] 📅 Study governance interventions (before/after analysis)
- [ ] 📅 Apply framework to other commons (Wikipedia, OpenStreetMap)

---

**Last Updated:** 2025-01-24
**Next Review:** Weekly on Mondays
