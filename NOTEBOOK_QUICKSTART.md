# Jupyter Notebook Quick Start

## Option 1: Install Packages in Notebook (Easiest)

Add this as **Cell 1** in your notebook:

```python
# Install required packages
import sys
!{sys.executable} -m pip install PyGithub tqdm python-dotenv --quiet
print("✅ Packages installed!")
```

## Option 2: Use Command to Set Token

In your terminal, before starting Jupyter:

```bash
export GITHUB_TOKEN="ghp_YOUR_TOKEN_HERE"
jupyter lab
```

Then in notebook cell 1:

```python
import os
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
print(f"✅ Token: {GITHUB_TOKEN[:7]}...{GITHUB_TOKEN[-4:]}")
```

## Option 3: Direct in Notebook (Quick Test)

```python
# Cell 1: Set token directly
GITHUB_TOKEN = "ghp_YOUR_TOKEN_HERE"

# Cell 2: Install and test
import sys
!{sys.executable} -m pip install PyGithub tqdm python-dotenv --quiet

# Cell 3: Test collector
import sys
sys.path.insert(0, '../src')

from collection.github_collector import GitHubCollector

collector = GitHubCollector(token=GITHUB_TOKEN)
print("✅ Collector initialized!")

# Cell 4: Quick test - check maintainers
maintainers = collector.collect_maintainer_data("curl/curl")
print(f"Active maintainers: {maintainers['statistics']['active_maintainers_6mo']}")
```

## Then Continue with Full Collection

```python
# Cell 5: Collect full dataset
data = collector.collect_complete_dataset("curl/curl", since_days=30)

# Cell 6: View summary
print(f"Stars: {data['repository']['stargazers_count']:,}")
print(f"Active maintainers: {data['maintainers']['statistics']['active_maintainers_6mo']}")
print(f"Contributors: {len(data['contributors'])}")
```

---

**Your current collector is running in background and will finish soon!**
Check progress: Look for file `data/raw/curl_curl_data.json`
