# Jupyter Notebook Quick Start

## Setup (Recommended)

**1. Copy the environment template:**
```bash
cp .env.example .env
```

**2. Edit `.env` and add your GitHub token:**
```bash
# Get a token at: https://github.com/settings/tokens
# Required scopes: public_repo, read:org, read:user
GITHUB_TOKEN=ghp_your_actual_token_here
```

**3. Start Jupyter:**
```bash
source venv/bin/activate
jupyter lab
```

The notebooks will automatically load from `.env` - no need to hardcode tokens!

---

## How Token Loading Works

All notebooks use this pattern:

```python
from pathlib import Path
from dotenv import load_dotenv

# Load from .env file in project root
env_path = Path("../.env")
if env_path.exists():
    load_dotenv(env_path)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
```

**Security:** The `.env` file is in `.gitignore` and will never be committed.

---

## Troubleshooting

**Token not found?**
1. Make sure `.env` exists in the project root
2. Check the token is not the placeholder `your_github_token_here`
3. Restart the Jupyter kernel after editing `.env`

**Rate limit issues?**
- Check remaining calls: `collector.get_rate_limit()`
- Wait for reset or use a different token

---

## Quick Test

Run this in any notebook to verify setup:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("../.env"))
token = os.getenv('GITHUB_TOKEN')

if token and token != "your_github_token_here":
    print(f"✅ Token loaded: {token[:7]}...{token[-4:]}")
else:
    print("❌ Token not configured - edit .env file")
```
