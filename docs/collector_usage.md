# GitHub Data Collector Usage Guide

Complete guide for using the enhanced GitHub data collector with PR/issue data.

## Setup

1. **Get GitHub Token:**
   ```bash
   # Create token at: https://github.com/settings/tokens
   # Required scopes: public_repo, read:org, read:user
   ```

2. **Configure Environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add: GITHUB_TOKEN=your_token_here
   ```

3. **Verify Setup:**
   ```bash
   python -c "from src.collection.github_collector import GitHubCollector; print('OK')"
   ```

---

## Basic Usage

### Collect Data for Single Project

```bash
# Command line usage
python src/collection/github_collector.py curl/curl

# With custom parameters
python src/collection/github_collector.py curl/curl --days 180 --output-dir data/raw
```

### Programmatic Usage

```python
from src.collection.github_collector import GitHubCollector
from pathlib import Path

# Initialize collector
collector = GitHubCollector()

# Collect complete dataset
data = collector.collect_complete_dataset("curl/curl", since_days=365)

# Save to file
output_path = Path("data/raw/curl_curl_data.json")
collector.save_data(data, output_path)
```

---

## Data Collection Methods

### 1. Repository Metrics

```python
metrics = collector.collect_repository_metrics("curl/curl")

# Returns:
{
    "name": "curl",
    "full_name": "curl/curl",
    "description": "...",
    "stargazers_count": 35000,
    "forks_count": 6000,
    "language": "C",
    "created_at": "...",
    "updated_at": "...",
    ...
}
```

### 2. Maintainer Identification

```python
maintainers = collector.collect_maintainer_data("curl/curl")

# Returns:
{
    "collaborators": [
        {"login": "bagder", "permissions": {...}}
    ],
    "codeowners": "# contents of CODEOWNERS file",
    "top_committers": [
        {"login": "bagder", "commits_6mo": 500}
    ],
    "statistics": {
        "total_collaborators": 5,
        "active_maintainers_6mo": 2  # >= 5 commits in 6 months
    }
}
```

**Key for Stadium Classification:**
- `active_maintainers_6mo` should be ≤3
- Check `top_committers` for dominance patterns

### 3. Contributor Data

```python
contributors = collector.collect_contributor_data("curl/curl", max_contributors=100)

# Returns list:
[
    {
        "login": "bagder",
        "contributions": 8000,
        "type": "User"
    },
    ...
]
```

**Use for Entropy Calculation:**
- Calculate contributor entropy from `contributions` distribution
- Identify concentration patterns (Stadium indicator)

### 4. Pull Request Data

```python
prs = collector.collect_pull_request_data("curl/curl", since_days=365, max_prs=200)

# Returns:
{
    "merged": [
        {
            "number": 12345,
            "title": "Fix memory leak",
            "created_at": "...",
            "merged_at": "...",
            "author": "contributor1",
            "comments": 5,
            "review_comments": 3,
            "mergeable_state": "clean",
            ...
        }
    ],
    "closed_unmerged": [...],
    "open": [...],
    "statistics": {
        "total_prs": 150,
        "merged_count": 120,
        "avg_time_to_merge": 24.5,  # hours
        "avg_comments_per_pr": 4.2,
        "conflict_rate": 0.15  # 15% had conflicts
    }
}
```

**VSM System 2 (Coordination) Indicators:**
- `avg_time_to_merge` - coordination efficiency
- `conflict_rate` - coordination health
- `avg_comments_per_pr` - review intensity

### 5. Issue Data

```python
issues = collector.collect_issue_data("curl/curl", since_days=365, max_issues=200)

# Returns:
{
    "closed": [
        {
            "number": 10000,
            "title": "Bug in HTTP/2",
            "created_at": "...",
            "closed_at": "...",
            "author": "user1",
            "comments": 8,
            "labels": ["bug", "http2"]
        }
    ],
    "open": [...],
    "statistics": {
        "total_issues": 180,
        "closed_count": 150,
        "avg_time_to_close": 72.3,  # hours
        "avg_comments_per_issue": 5.1,
        "bug_count": 80,
        "enhancement_count": 60,
        "question_count": 20
    }
}
```

**VSM System 1 (Operations) Indicators:**
- `avg_time_to_close` - operational responsiveness
- Issue resolution rate - operational health

### 6. Commit History

```python
commits = collector.collect_commit_history("curl/curl", since_days=365)

# Returns list:
[
    {
        "sha": "abc123",
        "author": "Daniel Stenberg",
        "author_login": "bagder",
        "date": "...",
        "message": "Fix SSL bug",
        "additions": 15,
        "deletions": 8,
        "total_changes": 23
    }
]
```

**Use for:**
- Temporal entropy calculation
- Activity patterns
- VSM S1 operational health

### 7. Governance Files

```python
gov_files = collector.check_governance_files("curl/curl")

# Returns:
{
    "GOVERNANCE.md": False,
    "CONTRIBUTING.md": True,
    "CODE_OF_CONDUCT.md": True,
    "SECURITY.md": True,
    "MAINTAINERS.md": False,
    ".github/CODEOWNERS": False
}
```

**Ostrom Principles Assessment:**
- CONTRIBUTING.md → Principle 2 (Congruence)
- CODE_OF_CONDUCT.md → Principle 6 (Conflict Resolution)
- GOVERNANCE.md → Principle 7 (Recognition of Rights)

---

## Complete Collection Workflow

### For Stadium Projects

```python
from src.collection.github_collector import GitHubCollector
from pathlib import Path

collector = GitHubCollector()

# List of Stadium candidates
stadium_projects = [
    "curl/curl",
    "zloirock/core-js",
    "psf/requests",
    "chalk/chalk",
    "uuid/uuid"
]

for repo in stadium_projects:
    print(f"\nCollecting: {repo}")

    try:
        # Collect complete dataset
        data = collector.collect_complete_dataset(repo, since_days=365)

        # Save data
        output_path = Path("data/raw") / f"{repo.replace('/', '_')}_data.json"
        collector.save_data(data, output_path)

        # Quick validation - check if Stadium criteria met
        active_maintainers = data['maintainers']['statistics']['active_maintainers_6mo']
        stars = data['repository']['stargazers_count']

        print(f"✓ Collected: {repo}")
        print(f"  Active maintainers: {active_maintainers}")
        print(f"  Stars: {stars}")

        if active_maintainers <= 3:
            print(f"  ✓ STADIUM CRITERIA MET")
        else:
            print(f"  ⚠ TOO MANY MAINTAINERS (not Stadium)")

    except Exception as e:
        print(f"✗ Error collecting {repo}: {e}")
        continue

    # Check rate limits
    rate_limit = collector.get_rate_limit()
    if rate_limit['core']['remaining'] < 500:
        print(f"\n⚠ Rate limit low: {rate_limit['core']['remaining']} remaining")
        print(f"Waiting until: {rate_limit['core']['reset']}")
        # Wait or pause collection
```

---

## Rate Limit Management

### Check Current Limits

```python
rate_limit = collector.get_rate_limit()

print(f"Core API: {rate_limit['core']['remaining']}/{rate_limit['core']['limit']}")
print(f"Search API: {rate_limit['search']['remaining']}/{rate_limit['search']['limit']}")
print(f"Resets at: {rate_limit['core']['reset']}")
```

### Strategies

1. **Automatic waiting** (built-in):
   - Collector automatically waits when limits are low
   - Checks every 50-100 items

2. **Multiple tokens:**
   ```python
   tokens = ["token1", "token2", "token3"]
   collectors = [GitHubCollector(token) for token in tokens]

   # Round-robin token usage
   for i, repo in enumerate(projects):
       collector = collectors[i % len(collectors)]
       data = collector.collect_complete_dataset(repo)
   ```

3. **Caching** (planned):
   - Cache API responses to avoid repeated calls
   - Update incrementally

---

## Data Validation

### After Collection

```python
def validate_stadium_project(data):
    """Validate if project meets Stadium criteria."""

    # 1. Check maintainer count
    active_maintainers = data['maintainers']['statistics']['active_maintainers_6mo']
    if active_maintainers > 3:
        return False, f"Too many maintainers: {active_maintainers}"

    # 2. Check activity (recent commits)
    if len(data['recent_commits']) < 10:
        return False, "Not active enough"

    # 3. Check impact (stars as proxy)
    stars = data['repository']['stargazers_count']
    if stars < 1000:  # Adjustable threshold
        return False, f"Low impact: {stars} stars"

    # 4. Check for performance data availability
    # (later: check package registry integration)

    return True, "Meets Stadium criteria"

# Use:
is_valid, message = validate_stadium_project(data)
print(f"Stadium validation: {message}")
```

---

## Output Data Structure

Complete dataset JSON structure:

```json
{
    "metadata": {
        "repo": "curl/curl",
        "collected_at": "2025-01-24T...",
        "collection_period_days": 365
    },
    "repository": { ... },
    "maintainers": {
        "collaborators": [...],
        "codeowners": "...",
        "top_committers": [...],
        "statistics": { ... }
    },
    "contributors": [...],
    "recent_commits": [...],
    "pull_requests": {
        "merged": [...],
        "closed_unmerged": [...],
        "open": [...],
        "statistics": { ... }
    },
    "issues": {
        "closed": [...],
        "open": [...],
        "statistics": { ... }
    },
    "governance_files": { ... }
}
```

---

## Next Steps

1. **Package Registry Integration:**
   - npm download stats
   - PyPI download stats
   - crates.io download stats

2. **Entropy Calculation:**
   - Use contributor data
   - Use commit patterns
   - Use PR/issue data

3. **VSM Scoring:**
   - Map metrics to VSM systems
   - Calculate health scores

4. **Batch Collection:**
   - Collect all 70 projects
   - Parallel collection with multiple tokens
   - Progress tracking

---

## Troubleshooting

### Permission Denied

```
Error: 403 {'message': 'Resource not accessible by integration'}
```

**Solution:** Token needs correct scopes (public_repo, read:org, read:user)

### Rate Limit Exceeded

```
Error: RateLimitExceededException
```

**Solution:**
- Wait for reset (automatic in collector)
- Use multiple tokens
- Reduce max_prs/max_issues parameters

### Repository Not Found

```
Error: 404 {'message': 'Not Found'}
```

**Solution:**
- Check repository name format (owner/repo)
- Ensure repository is public
- Verify token has access

---

## Performance Tips

1. **Reduce scope for faster collection:**
   ```python
   # Collect only last 90 days instead of 365
   data = collector.collect_complete_dataset(repo, since_days=90)
   ```

2. **Limit sample sizes:**
   ```python
   # Reduce max items collected
   prs = collector.collect_pull_request_data(repo, max_prs=100)  # instead of 200
   issues = collector.collect_issue_data(repo, max_issues=100)
   ```

3. **Skip less critical data:**
   - Collect governance files separately (fast)
   - Focus on maintainer + PR/issue data for initial analysis

---

---

## Batch Collection with Daemon CLI

The collector daemon provides a robust CLI for automated batch collection with rate limit management.

### Quick Start

```bash
# 1. Initialize queue with stadium projects
make collector-init CATEGORY=stadium

# 2. Check status
make collector-status

# 3. Start collection (stops at rate limit)
make collector-run LIMIT=10

# 4. Monitor progress in real-time
make collector-watch

# 5. Resume after rate limit resets
make collector-resume
```

### Available Commands

| Command | Description |
|---------|-------------|
| `make collector-init CATEGORY=stadium` | Initialize queue for a category (stadium, federation, club, toy) |
| `make collector-status` | Show current collection status |
| `make collector-watch` | Live dashboard that updates every 5s (Ctrl+C to exit) |
| `make collector-run LIMIT=10` | Collect N projects, stops when rate limit low |
| `make collector-run-wait LIMIT=10` | Collect N projects, waits for rate limit reset |
| `make collector-resume` | Continue collection from where it stopped |
| `make collector-retry` | Retry failed projects |
| `make collector-clear` | Clear collection state (start fresh) |

### Configuration

**Environment Variables:**

```bash
# .env file
GITHUB_TOKEN=ghp_xxx                    # Required: single token
GITHUB_TOKENS=ghp_token1,ghp_token2     # Optional: multiple tokens for 2-3x throughput
```

**Make Variables:**

```bash
# Set category (default: stadium)
make collector-init CATEGORY=federation

# Set collection limit (default: 10)
make collector-run LIMIT=20

# Set watch interval (default: 5 seconds)
make collector-watch WATCH_INTERVAL=10
```

### Workflow Examples

**1. Full Category Collection (Unattended)**

```bash
# Initialize
make collector-init CATEGORY=stadium

# Run with auto-wait (will wait for rate limit and continue)
make collector-run-wait LIMIT=999

# In another terminal, monitor progress
make collector-watch
```

**2. Incremental Collection (Manual)**

```bash
# Initialize
make collector-init CATEGORY=stadium

# Collect in batches
make collector-run LIMIT=10
# Wait 45-60 minutes for rate limit reset
make collector-resume LIMIT=10
# Repeat until complete
```

**3. Recovering from Failures**

```bash
# Check status to see failed projects
make collector-status

# Retry all failed projects
make collector-retry

# Continue collection
make collector-resume
```

### State File

Collection progress is persisted in `data/collection_state.json`:

```json
{
  "queue": {
    "pending": ["owner/repo1", "owner/repo2"],
    "in_progress": null,
    "completed": ["curl/curl", "nodejs/node"],
    "failed": [{"repo": "...", "error": "...", "timestamp": "..."}]
  },
  "metadata": {
    "category": "stadium",
    "total_projects": 70,
    "created_at": "...",
    "updated_at": "..."
  },
  "statistics": {
    "api_calls_total": 12500,
    "collections_completed": 35
  }
}
```

### Rate Limit Strategy

- **Single token:** ~14 projects/hour (5000 calls/hour ÷ 350 calls/project)
- **Two tokens:** ~28 projects/hour
- **Minimum threshold:** Collection stops when remaining < 500 calls

The daemon automatically:
1. Checks rate limit before each project
2. Stops gracefully when limit is low
3. Saves progress for easy resumption
4. Handles Ctrl+C gracefully

---

## AWS Deployment (Phase 2)

For fully automated collection, deploy to AWS using CDK.

### Prerequisites

```bash
# Install CDK dependencies
cd infra && npm install

# Bootstrap CDK (first time only)
make cdk-bootstrap

# Store GitHub token in SSM
GITHUB_TOKEN=ghp_xxx make cdk-set-token
```

### CDK Commands

| Command | Description |
|---------|-------------|
| `make cdk-bootstrap` | Bootstrap CDK in your AWS account (first time) |
| `make cdk-synth` | Synthesize CloudFormation template |
| `make cdk-diff` | Preview infrastructure changes |
| `make cdk-deploy` | Deploy to AWS |
| `make cdk-destroy` | Destroy all AWS resources |
| `make cdk-set-token` | Store GitHub token in SSM Parameter Store |

### Architecture

```
EventBridge Scheduler (hourly)
         │
         ▼
    Lambda Function
    (14 min timeout)
         │
    ┌────┴────┐
    │         │
    ▼         ▼
DynamoDB    S3 Bucket
 (state)    (data)
```

### Syncing Data Locally

After deployment, sync collected data:

```bash
aws s3 sync s3://categories-of-the-commons-data-{ACCOUNT_ID}/raw data/raw
```

---

**Last Updated:** 2025-11-28
