#!/bin/bash
# Setup script for GitHub token

echo "🔑 GitHub Token Setup"
echo "====================="
echo ""
echo "To collect data from GitHub, you need a personal access token."
echo ""
echo "Steps:"
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Give it a name: 'categories-of-the-commons'"
echo "4. Select scopes:"
echo "   ✓ public_repo"
echo "   ✓ read:org"
echo "   ✓ read:user"
echo "5. Click 'Generate token'"
echo "6. Copy the token (starts with 'ghp_')"
echo ""
echo "Then run:"
echo "  export GITHUB_TOKEN='your_token_here'"
echo ""
echo "Or add it to .env file:"
echo "  GITHUB_TOKEN=your_token_here"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if token is already set
if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "✓ GITHUB_TOKEN is already set in environment"
    echo ""
    echo "Testing token..."
    python3 -c "
from github import Github
import os
token = os.getenv('GITHUB_TOKEN')
if token:
    try:
        g = Github(token)
        user = g.get_user()
        print(f'✓ Token valid! Authenticated as: {user.login}')
        rate = g.get_rate_limit()
        print(f'✓ Rate limit: {rate.core.remaining}/{rate.core.limit} remaining')
    except Exception as e:
        print(f'✗ Token invalid or expired: {e}')
else:
    print('✗ No token found')
" 2>/dev/null || echo "⚠ Could not verify token (PyGithub not installed?)"
else
    echo "⚠ GITHUB_TOKEN not set"
    echo ""
    echo "After creating your token, run:"
    echo "  export GITHUB_TOKEN='your_token_here'"
    echo "  ./scripts/setup_token.sh  # to verify"
fi
