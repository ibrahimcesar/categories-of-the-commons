# Stadium Project Candidates

Research list for identifying Stadium projects meeting criteria:
- **High downloads:** >100k/month (npm), >1M total (PyPI), >10M (crates.io)
- **≤3 core maintainers**
- **Active:** commits in last 6 months
- **Impact:** Real organizational/infrastructure usage

---

## Data Collection Status

**Collected:** 12 projects | **Target:** 28 projects

---

## Confirmed Stadium Projects (3)

### 1. curl [DATA COLLECTED]
- **Repo:** curl/curl
- **Language:** C
- **Maintainers:** 1 (Daniel Stenberg)
- **Usage:** Billions of installs, core internet infrastructure
- **Rationale:** Iconic Stadium, single maintainer, massive global impact
- **Status:** CONFIRMED | **Classification:** Stadium (Strong)

### 2. core-js [DATA COLLECTED]
- **Repo:** zloirock/core-js
- **Language:** JavaScript
- **Maintainers:** 1 (Denis Pushkarev / zloirock)
- **Usage:** >1 billion npm downloads/month
- **Rationale:** Critical infrastructure, maintainer burnout story, controversial
- **Status:** CONFIRMED

### 3. requests [DATA COLLECTED]
- **Repo:** psf/requests
- **Language:** Python
- **Maintainers:** 2-3 (Kenneth Reitz legacy, current small team)
- **Usage:** >500M PyPI downloads, most popular Python HTTP library
- **Rationale:** Standard library alternative, high impact, minimal team
- **Status:** CONFIRMED

---

## High-Priority Candidates (Need Verification)

### JavaScript/Node.js

#### HTTP & Networking
- [x] **axios** (axios/axios) [DATA COLLECTED]
  - Downloads: ~50M/week npm
  - Maintainers: Need to verify (appears 2-3)
  - Usage: Most popular HTTP client
  - *Action: Verify maintainer count*

- [ ] **node-fetch** (node-fetch/node-fetch)
  - Downloads: ~30M/week npm
  - Maintainers: Need to verify
  - Usage: Fetch API for Node.js
  - *Action: Verify maintainer count*

- [x] **got** (sindresorhus/got) [DATA COLLECTED]
  - Downloads: ~15M/week npm
  - Maintainers: 1-2 (Sindre Sorhus primary)
  - Usage: Modern HTTP client
  - **Classification:** Stadium (Likely)

#### CLI Utilities
- [x] **chalk** (chalk/chalk) [DATA COLLECTED]
  - Downloads: ~80M/week npm
  - Maintainers: 1-2 (Sindre Sorhus primary)
  - Usage: Terminal string styling, used everywhere
  - **Classification:** Stadium (Likely)

- [x] **commander** (tj/commander.js) [DATA COLLECTED]
  - Downloads: ~70M/week npm
  - Maintainers: 2-3 (TJ Holowaychuk legacy)
  - Usage: CLI argument parsing standard
  - **Classification:** Stadium (Strong)

- [ ] **yargs** (yargs/yargs)
  - Downloads: ~50M/week npm
  - Maintainers: Need to verify
  - Usage: CLI parser alternative
  - *Action: Verify maintainer count*

#### Babel Ecosystem
- [ ] **@babel/core** (babel/babel monorepo)
  - Downloads: ~40M/week npm
  - Maintainers: Small team (~3?)
  - Usage: JavaScript transpiler, critical infrastructure
  - *Action: Verify if small enough team*

- [ ] **@babel/preset-env**
  - Part of Babel monorepo
  - Same team as core
  - *Action: Research maintainer structure*

#### Utilities
- [ ] **uuid** (uuidjs/uuid)
  - Downloads: ~60M/week npm
  - Maintainers: Need to verify
  - Usage: UUID generation standard
  - *Action: HIGH PRIORITY - Check maintainers*

- [ ] **ms** (vercel/ms)
  - Downloads: ~90M/week npm (dependency of many)
  - Maintainers: 1-2 (Vercel maintained)
  - Usage: Time parsing utility
  - *Action: Verify and confirm*

- [ ] **debug** (debug-js/debug)
  - Downloads: ~80M/week npm
  - Maintainers: Need to verify
  - Usage: Debugging utility used everywhere
  - *Action: Check maintainer count*

- [ ] **semver** (npm/node-semver)
  - Downloads: ~90M/week npm
  - Maintainers: npm team (need count)
  - Usage: Semantic versioning parser
  - *Action: Verify maintainer count*

### Python

#### Web & HTTP
- [ ] **urllib3** (urllib3/urllib3)
  - Downloads: ~200M/month PyPI
  - Maintainers: 2-3 (small core team)
  - Usage: Low-level HTTP library, requests dependency
  - *Action: HIGH PRIORITY - Verify maintainers*

- [ ] **certifi** (certifi/python-certifi)
  - Downloads: ~200M/month PyPI
  - Maintainers: Small team
  - Usage: SSL certificate bundle
  - *Action: Verify maintainer count*

#### CLI & Utilities
- [ ] **click** (pallets/click)
  - Downloads: ~100M/month PyPI
  - Maintainers: Pallets team (need count)
  - Usage: CLI framework standard
  - *Action: Verify maintainer count*

- [ ] **python-dateutil** (dateutil/dateutil)
  - Downloads: ~150M/month PyPI
  - Maintainers: 1-2 maintainers
  - Usage: Date parsing/manipulation
  - *Action: HIGH PRIORITY - Likely candidate*

- [x] **six** (benjaminp/six) [DATA COLLECTED]
  - Downloads: ~200M/month PyPI
  - Maintainers: 1 (Benjamin Peterson)
  - Usage: Python 2/3 compatibility (legacy but still used)
  - **Classification:** Stadium (Strong)

#### Data & Serialization
- [x] **PyYAML** (yaml/pyyaml) [DATA COLLECTED]
  - Downloads: ~150M/month PyPI
  - Maintainers: Small team
  - Usage: YAML parser standard
  - **Classification:** Stadium (Likely)

- [ ] **attrs** (python-attrs/attrs)
  - Downloads: ~50M/month PyPI
  - Maintainers: 2-3 maintainers
  - Usage: Class definition library
  - *Action: Verify maintainer count*

### Rust

#### Serialization
- [x] **serde** (serde-rs/serde) [DATA COLLECTED]
  - Downloads: ~200M all-time crates.io
  - Maintainers: 1-2 (dtolnay primary)
  - Usage: Serialization framework, used by everything
  - **Classification:** Stadium (Strong)

- [ ] **serde_json** (serde-rs/json)
  - Downloads: ~180M all-time
  - Maintainers: Same as serde
  - Usage: JSON serialization
  - *Action: Part of serde ecosystem*

#### Async & Networking
- [ ] **tokio** (tokio-rs/tokio)
  - Downloads: ~100M all-time
  - Maintainers: Small core team
  - Usage: Async runtime standard
  - *Action: Verify if maintainer count qualifies*

- [ ] **tokio components** (Various sub-crates)
  - May have smaller teams
  - *Action: Research individual component maintainers*

#### CLI & Utils
- [ ] **clap** (clap-rs/clap)
  - Downloads: ~100M all-time
  - Maintainers: Small team
  - Usage: CLI parser standard
  - *Action: Verify maintainer count*

- [ ] **regex** (rust-lang/regex)
  - Downloads: ~150M all-time
  - Maintainers: 1-2 (BurntSushi primary)
  - Usage: Regex engine
  - *Action: HIGH PRIORITY - Likely candidate*

- [ ] **rand** (rust-random/rand)
  - Downloads: ~120M all-time
  - Maintainers: Small team
  - Usage: Random number generation
  - *Action: Verify maintainer count*

### C/C++

#### Infrastructure
- [ ] **SQLite** (sqlite/sqlite)
  - Usage: Billions of installs, most deployed database
  - Maintainers: 1-3 (D. Richard Hipp primary)
  - Rationale: Single author, massive global usage
  - *Action: HIGH PRIORITY - Classic Stadium*

- [x] **zlib** (madler/zlib) [DATA COLLECTED]
  - Usage: Universal compression library
  - Maintainers: 1-2 (Mark Adler)
  - Rationale: Core infrastructure, minimal team
  - **Classification:** Stadium (Strong)

- [x] **libpng** (glennrp/libpng) [DATA COLLECTED]
  - Usage: PNG image format reference implementation
  - Maintainers: Small team
  - **Classification:** Stadium (Strong)

#### Web Servers & Components
- [ ] **nginx modules** (Various)
  - Core nginx has small team
  - Individual modules may be Stadium
  - *Action: Research specific high-use modules*

### Go

#### Infrastructure
- [ ] **go-github** (google/go-github)
  - Usage: GitHub API client
  - Maintainers: Small team
  - *Action: Verify maintainer count*

- [ ] **gorilla/mux** (gorilla/mux)
  - Usage: HTTP router
  - Maintainers: Small team
  - *Action: Verify maintainer count*

- [ ] **cobra** (spf13/cobra)
  - Usage: CLI framework
  - Maintainers: Small team
  - *Action: Verify maintainer count*

### Ruby

- [ ] **rack** (rack/rack)
  - Usage: Web server interface standard
  - Maintainers: Small team
  - *Action: Verify maintainer count*

- [ ] **nokogiri** (sparklemotion/nokogiri)
  - Usage: XML/HTML parser
  - Maintainers: Small core team
  - *Action: Verify maintainer count*

---

## Collected Data Summary

| # | Project | Language | Classification | Stars | Contributors |
|---|---------|----------|----------------|-------|--------------|
| 1 | curl/curl | C | Stadium (Strong) | 37k+ | 100+ |
| 2 | zloirock/core-js | JavaScript | - | 24k+ | - |
| 3 | psf/requests | Python | - | 52k+ | - |
| 4 | axios/axios | JavaScript | - | 106k+ | - |
| 5 | chalk/chalk | JavaScript | Stadium (Likely) | 22k | 57 |
| 6 | sindresorhus/got | JavaScript | Stadium (Likely) | 14k | 100 |
| 7 | tj/commander.js | JavaScript | Stadium (Strong) | 27k | 100 |
| 8 | benjaminp/six | Python | Stadium (Strong) | 1k | 58 |
| 9 | yaml/pyyaml | Python | Stadium (Likely) | 2.8k | 37 |
| 10 | serde-rs/serde | Rust | Stadium (Strong) | 10k | 100 |
| 11 | madler/zlib | C | Stadium (Strong) | 6.5k | 54 |
| 12 | glennrp/libpng | C | Stadium (Strong) | 1.5k | 85 |

---

## Verification Checklist

For each candidate, verify:

1. **Maintainer Count**
   ```bash
   # GitHub API query
   curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/repos/OWNER/REPO/collaborators

   # Check CODEOWNERS file
   # Check recent commit authors (last 6 months)
   ```

2. **Download Metrics**
   - npm: https://www.npmjs.com/package/PACKAGE
   - PyPI: https://pypistats.org/packages/PACKAGE
   - crates.io: https://crates.io/crates/CRATE
   - Check weekly/monthly download counts

3. **Activity**
   ```bash
   # Check recent commits
   git log --since="6 months ago" --format="%an" | sort | uniq -c | sort -rn
   ```

4. **Impact Assessment**
   - Check dependent projects count
   - Research usage in major projects
   - Look for mentions in "most used" lists

---

## Research Strategy

### High-Priority Actions (Next 2 days)

1. **Verify Top 7 Candidates:**
   - ~~chalk (JavaScript)~~ COLLECTED
   - uuid (JavaScript)
   - urllib3 (Python)
   - python-dateutil (Python)
   - ~~serde (Rust)~~ COLLECTED
   - regex (Rust)
   - SQLite (C)

2. **Collect Data:**
   - Use github_collector.py to check maintainer count
   - Query package registries for downloads
   - Document rationale for each

3. **Reach First 10:**
   - Current: 12 collected
   - Target: 16 more needed
   - Milestone: REACHED

### Secondary Research (Week 2)

4. **Fill to 20:**
   - Verify medium-priority candidates
   - Expand to more languages if needed
   - Research niche but high-use libraries

5. **Complete to 28:**
   - Deep dive into language ecosystems
   - Check dependency graphs for hidden Stadium projects
   - Validate with community (Reddit, HackerNews)

---

## Alternative Sources

If struggling to find candidates:

### 1. Package Registry Analysis
- **npm:** Top 100 most depended-upon packages
  - Filter by small team size

- **PyPI:** Top downloads list
  - https://hugovk.github.io/top-pypi-packages/

- **crates.io:** Most downloaded crates
  - Filter by small maintainer count

### 2. Dependency Graph Mining
- Use Libraries.io data
- Identify transitive dependency patterns
- Find "invisible" infrastructure

### 3. "Bus Factor = 1" Lists
- Search GitHub for "bus factor"
- Critical projects with single maintainer
- Infrastructure projects at risk

### 4. Maintainer Burnout Stories
- Follow "Roads and Bridges" report
- Core-js-style cases
- Projects with maintainer funding requests

---

## Notes

**Threshold Flexibility:**
- If struggling to find 28 projects at >100k/month npm:
  - Lower to 50k/month for npm
  - Accept 500k total for PyPI
  - Accept 5M total for crates.io

**Maintainer Count:**
- Focus on "active" maintainers (commits in last 6 months)
- Exclude inactive/emeritus maintainers
- Count CODEOWNERS if present

**Language Balance:**
- Target: JavaScript (10), Python (8), Rust (5), C/C++ (3), Other (2)
- Ensures cross-language generalizability

---

**Last Updated:** 2025-11-25
**Next Review:** After reaching 20 projects
