#!/usr/bin/env python3
"""
VSM Health Badge Generator

Standalone script to generate VSM health badges for any GitHub repository.
Can be run locally or in CI/CD pipelines.

Usage:
    python scripts/generate_vsm_badge.py owner/repo
    python scripts/generate_vsm_badge.py owner/repo --output ./badges
    python scripts/generate_vsm_badge.py owner/repo --theme light

Environment:
    GITHUB_TOKEN - Optional, increases API rate limits

Examples:
    python scripts/generate_vsm_badge.py curl/curl
    python scripts/generate_vsm_badge.py grafana/grafana --output docs/badges
"""

import os
import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Run: pip install httpx")
    sys.exit(1)


# =============================================================================
# GitHub Data Fetcher
# =============================================================================

def fetch_github_data(owner: str, repo: str, token: str = None) -> dict:
    """Fetch project data from GitHub API."""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'

    with httpx.Client(timeout=30.0) as client:
        print(f"Fetching data for {owner}/{repo}...")

        # Repository info
        repo_resp = client.get(
            f'https://api.github.com/repos/{owner}/{repo}',
            headers=headers
        )
        if repo_resp.status_code == 404:
            print(f"Error: Repository {owner}/{repo} not found")
            sys.exit(1)
        if repo_resp.status_code == 403:
            print("Error: GitHub API rate limit exceeded. Set GITHUB_TOKEN environment variable.")
            sys.exit(1)
        repo_data = repo_resp.json()

        # Contributors
        contrib_resp = client.get(
            f'https://api.github.com/repos/{owner}/{repo}/contributors',
            headers=headers, params={'per_page': 30}
        )
        contributors = contrib_resp.json() if contrib_resp.status_code == 200 else []

        # Commits
        commits_resp = client.get(
            f'https://api.github.com/repos/{owner}/{repo}/commits',
            headers=headers, params={'per_page': 50}
        )
        commits = commits_resp.json() if commits_resp.status_code == 200 else []

        # Pull requests
        prs_resp = client.get(
            f'https://api.github.com/repos/{owner}/{repo}/pulls',
            headers=headers, params={'state': 'all', 'per_page': 30}
        )
        prs = prs_resp.json() if prs_resp.status_code == 200 else []

        # Governance files
        gov_files = {}
        files_to_check = [
            'GOVERNANCE.md', 'CODE_OF_CONDUCT.md', 'CONTRIBUTING.md',
            'MAINTAINERS.md', '.github/CODEOWNERS', 'ROADMAP.md'
        ]
        for f in files_to_check:
            resp = client.get(
                f'https://api.github.com/repos/{owner}/{repo}/contents/{f}',
                headers=headers
            )
            gov_files[f] = resp.status_code == 200

        return {
            'repository': repo_data,
            'contributors': contributors if isinstance(contributors, list) else [],
            'recent_commits': commits if isinstance(commits, list) else [],
            'pull_requests': prs if isinstance(prs, list) else [],
            'governance_files': gov_files,
        }


# =============================================================================
# VSM Score Calculator
# =============================================================================

def calculate_vsm_scores(data: dict, owner: str, repo: str) -> dict:
    """Calculate VSM health scores from GitHub data."""
    contributors = data.get('contributors', [])
    commits = data.get('recent_commits', [])
    prs = data.get('pull_requests', [])
    gov_files = data.get('governance_files', {})
    repo_data = data.get('repository', {})

    # Bus factor calculation
    if contributors:
        contribs = sorted([c.get('contributions', 0) for c in contributors], reverse=True)
        total = sum(contribs)
        cumsum, bus_factor = 0, 0
        for c in contribs:
            cumsum += c
            bus_factor += 1
            if cumsum >= total * 0.5:
                break
    else:
        bus_factor = 0

    # S1: Operations (25%)
    s1 = min(100,
        min(30, len(contributors) * 0.5) +
        min(25, len(commits) * 0.5) +
        min(25, len(prs) * 0.5) +
        min(20, bus_factor * 5)
    )

    # S2: Coordination (20%)
    s2 = 0
    s2 += 30 if gov_files.get('.github/CODEOWNERS') else 0
    s2 += 40 if prs else 0
    s2 += 30 if len(prs) > 5 else 15
    s2 = min(100, s2)

    # S3: Control (20%)
    s3 = 0
    s3 += 25 if gov_files.get('CONTRIBUTING.md') else 0
    s3 += 25 if gov_files.get('MAINTAINERS.md') else 0
    active_maintainers = min(5, len([c for c in contributors[:10] if c.get('contributions', 0) > 10]))
    s3 += min(50, active_maintainers * 12.5)
    s3 = min(100, s3)

    # S4: Intelligence (15%)
    s4 = 0
    s4 += 30 if repo_data.get('has_discussions') else 0
    s4 += 30 if gov_files.get('ROADMAP.md') else 0
    s4 += 20 if repo_data.get('has_wiki') else 0
    s4 += 20 if repo_data.get('open_issues_count', 0) > 0 else 0
    s4 = min(100, s4)

    # S5: Policy (20%)
    s5 = 0
    s5 += 30 if gov_files.get('GOVERNANCE.md') else 0
    s5 += 20 if gov_files.get('CODE_OF_CONDUCT.md') else 0
    s5 += 20 if repo_data.get('license') else 0
    s5 += 10 if repo_data.get('description') else 0
    owner_login = repo_data.get('owner', {}).get('login', '').lower()
    foundation_indicators = ['apache', 'linux', 'cncf', 'eclipse', 'python']
    s5 += 20 if any(f in owner_login for f in foundation_indicators) else 0
    s5 = min(100, s5)

    # Overall score (weighted)
    overall = s1 * 0.25 + s2 * 0.20 + s3 * 0.20 + s4 * 0.15 + s5 * 0.20

    # Risk level
    scores = [s1, s2, s3, s4, s5]
    critical_count = sum(1 for s in scores if s < 40)
    if critical_count >= 2 or overall < 30:
        risk_level = 'CRITICAL'
    elif critical_count >= 1 or overall < 50:
        risk_level = 'HIGH'
    elif overall < 70:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'

    # Category
    if overall >= 60 and len(contributors) > 50:
        category = 'federation'
    elif overall >= 45 and len(contributors) > 20:
        category = 'club'
    elif len(contributors) > 5:
        category = 'stadium'
    else:
        category = 'toy'

    def get_status(score):
        if score >= 70:
            return 'healthy'
        elif score >= 40:
            return 'warning'
        return 'critical'

    return {
        'repository': f'{owner}/{repo}',
        'overall_score': overall,
        'risk_level': risk_level,
        'category': category,
        'subsystems': {
            'S1': {'score': s1, 'status': get_status(s1), 'name': 'Operations'},
            'S2': {'score': s2, 'status': get_status(s2), 'name': 'Coordination'},
            'S3': {'score': s3, 'status': get_status(s3), 'name': 'Control'},
            'S4': {'score': s4, 'status': get_status(s4), 'name': 'Intelligence'},
            'S5': {'score': s5, 'status': get_status(s5), 'name': 'Policy'},
        },
        'indicators': {
            'contributors': len(contributors),
            'bus_factor': bus_factor,
            'has_codeowners': gov_files.get('.github/CODEOWNERS', False),
            'has_governance': gov_files.get('GOVERNANCE.md', False),
            'has_contributing': gov_files.get('CONTRIBUTING.md', False),
            'has_coc': gov_files.get('CODE_OF_CONDUCT.md', False),
        },
        'generated_at': datetime.now().isoformat(),
    }


# =============================================================================
# SVG Badge Generators
# =============================================================================

def get_score_color(score: float) -> str:
    if score >= 70:
        return '#2ecc71'
    elif score >= 40:
        return '#f39c12'
    return '#e74c3c'


RISK_COLORS = {
    'LOW': '#2ecc71',
    'MEDIUM': '#f1c40f',
    'HIGH': '#e67e22',
    'CRITICAL': '#e74c3c'
}


def generate_simple_badge(report: dict) -> str:
    """Generate shields.io style badge."""
    score = int(report['overall_score'])
    color = get_score_color(report['overall_score'])

    label = "VSM Health"
    label_width = len(label) * 7 + 10
    value_width = len(str(score)) * 9 + 10
    total_width = label_width + value_width

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <linearGradient id="smooth" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="round">
    <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#round)">
    <rect width="{label_width}" height="20" fill="#555"/>
    <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
    <rect width="{total_width}" height="20" fill="url(#smooth)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_width/2}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_width/2}" y="14">{label}</text>
    <text x="{label_width + value_width/2}" y="15" fill="#010101" fill-opacity=".3">{score}</text>
    <text x="{label_width + value_width/2}" y="14">{score}</text>
  </g>
</svg>'''


def generate_detailed_card(report: dict, theme: str = 'dark') -> str:
    """Generate detailed health card."""
    width, height, padding = 400, 280, 20

    if theme == 'dark':
        bg_color = '#1a1a2e'
        text_color = '#ffffff'
        text_secondary = '#a0a0a0'
        border_color = '#333355'
        gradient_end = '#16213e'
    else:
        bg_color = '#ffffff'
        text_color = '#333333'
        text_secondary = '#666666'
        border_color = '#e1e4e8'
        gradient_end = '#f6f8fa'

    subsystems = ['S1', 'S2', 'S3', 'S4', 'S5']
    names = ['Operations', 'Coordination', 'Control', 'Intelligence', 'Policy']

    score_color = get_score_color(report['overall_score'])
    risk_color = RISK_COLORS.get(report['risk_level'], '#888')

    bars_svg = ""
    bar_y_start, bar_height, bar_spacing = 100, 8, 30
    bar_width = width - 2 * padding - 120

    for i, (key, name) in enumerate(zip(subsystems, names)):
        sub = report['subsystems'][key]
        y = bar_y_start + i * bar_spacing
        filled = (sub['score'] / 100) * bar_width
        bar_color = get_score_color(sub['score'])

        bars_svg += f'''
    <text x="{padding}" y="{y + 6}" font-size="12" fill="{text_color}">{key}: {name}</text>
    <rect x="{padding + 120}" y="{y - 4}" width="{bar_width}" height="{bar_height}" rx="4" fill="{border_color}"/>
    <rect x="{padding + 120}" y="{y - 4}" width="{filled}" height="{bar_height}" rx="4" fill="{bar_color}"/>
    <text x="{padding + 125 + bar_width}" y="{y + 6}" font-size="11" fill="{text_secondary}">{sub['score']:.0f}</text>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{gradient_end};stop-opacity:1" />
    </linearGradient>
  </defs>

  <rect width="{width}" height="{height}" rx="10" fill="url(#cardGrad)" stroke="{border_color}" stroke-width="1"/>

  <text x="{padding}" y="{padding + 20}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="18" font-weight="bold" fill="{text_color}">VSM Health Report</text>
  <text x="{padding}" y="{padding + 40}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="12" fill="{text_secondary}">{report['repository']}</text>

  <circle cx="{width - 60}" cy="{padding + 30}" r="30" fill="none" stroke="{border_color}" stroke-width="4"/>
  <circle cx="{width - 60}" cy="{padding + 30}" r="30" fill="none" stroke="{score_color}" stroke-width="4"
          stroke-dasharray="{report['overall_score'] * 1.88} 188" stroke-linecap="round" transform="rotate(-90 {width - 60} {padding + 30})"/>
  <text x="{width - 60}" y="{padding + 35}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="16" font-weight="bold" fill="{text_color}" text-anchor="middle">{report['overall_score']:.0f}</text>

  <rect x="{width - 100}" y="{padding + 55}" width="80" height="20" rx="10" fill="{risk_color}"/>
  <text x="{width - 60}" y="{padding + 69}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10" fill="white" text-anchor="middle">{report['risk_level']}</text>

  {bars_svg}

  <text x="{padding}" y="{height - 15}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10" fill="{text_secondary}">Category: {report['category'].title()}</text>
  <text x="{width - padding}" y="{height - 15}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="end">Generated: {datetime.now().strftime('%Y-%m-%d')}</text>
</svg>'''


def generate_mini_card(report: dict, theme: str = 'dark') -> str:
    """Generate compact mini card with radar."""
    width, height = 250, 80

    if theme == 'dark':
        bg_color = '#1a1a2e'
        text_secondary = '#a0a0a0'
        border_color = '#333355'
    else:
        bg_color = '#ffffff'
        text_secondary = '#666666'
        border_color = '#e1e4e8'

    score_color = get_score_color(report['overall_score'])

    # Radar points
    cx, cy, r = 45, 45, 25
    scores = [report['subsystems'][s]['score'] for s in ['S1', 'S2', 'S3', 'S4', 'S5']]
    points = []
    for i, score in enumerate(scores):
        angle = (i * 72 - 90) * math.pi / 180
        point_r = r * (score / 100)
        x = cx + point_r * math.cos(angle)
        y = cy + point_r * math.sin(angle)
        points.append(f"{x},{y}")
    points_str = " ".join(points)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" rx="8" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{border_color}" stroke-width="1" opacity="0.3"/>
  <circle cx="{cx}" cy="{cy}" r="{r*0.5}" fill="none" stroke="{border_color}" stroke-width="1" opacity="0.2"/>

  <polygon points="{points_str}" fill="{score_color}" fill-opacity="0.3" stroke="{score_color}" stroke-width="2"/>

  <text x="95" y="25" font-family="Segoe UI, Ubuntu, sans-serif" font-size="11" fill="{text_secondary}">VSM Health</text>
  <text x="95" y="50" font-family="Segoe UI, Ubuntu, sans-serif" font-size="28" font-weight="bold" fill="{score_color}">{report['overall_score']:.0f}</text>
  <text x="135" y="50" font-family="Segoe UI, Ubuntu, sans-serif" font-size="12" fill="{text_secondary}">/100</text>
  <text x="95" y="68" font-family="Segoe UI, Ubuntu, sans-serif" font-size="10" fill="{text_secondary}">{report['category'].title()} | {report['risk_level']}</text>
</svg>'''


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate VSM health badges for GitHub repositories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_vsm_badge.py curl/curl
  python generate_vsm_badge.py grafana/grafana --output ./badges
  python generate_vsm_badge.py owner/repo --theme light --json

Environment Variables:
  GITHUB_TOKEN    Optional GitHub token for higher API rate limits
        '''
    )
    parser.add_argument('repository', help='GitHub repository (owner/repo)')
    parser.add_argument('--output', '-o', default='./docs/badges', help='Output directory (default: ./docs/badges)')
    parser.add_argument('--theme', '-t', choices=['dark', 'light'], default='dark', help='Card theme (default: dark)')
    parser.add_argument('--json', action='store_true', help='Also output JSON report')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output')

    args = parser.parse_args()

    # Parse repository
    if '/' not in args.repository:
        print("Error: Repository must be in format owner/repo")
        sys.exit(1)

    owner, repo = args.repository.split('/', 1)
    token = os.environ.get('GITHUB_TOKEN')

    # Fetch data and calculate scores
    data = fetch_github_data(owner, repo, token)
    report = calculate_vsm_scores(data, owner, repo)

    if not args.quiet:
        print(f"\nVSM Health Report for {owner}/{repo}")
        print("=" * 50)
        print(f"Overall Score: {report['overall_score']:.1f}")
        print(f"Risk Level:    {report['risk_level']}")
        print(f"Category:      {report['category'].title()}")
        print("\nSubsystem Scores:")
        for key in ['S1', 'S2', 'S3', 'S4', 'S5']:
            sub = report['subsystems'][key]
            status_icon = {'healthy': '+', 'warning': '~', 'critical': '-'}[sub['status']]
            print(f"  [{status_icon}] {key} ({sub['name']}): {sub['score']:.0f}")

    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate and save badges
    safe_name = args.repository.replace('/', '_')

    # Simple badge
    badge = generate_simple_badge(report)
    badge_path = output_dir / f'{safe_name}_badge.svg'
    badge_path.write_text(badge)
    if not args.quiet:
        print(f"\nSaved: {badge_path}")

    # Detailed card
    card = generate_detailed_card(report, args.theme)
    card_path = output_dir / f'{safe_name}_card.svg'
    card_path.write_text(card)
    if not args.quiet:
        print(f"Saved: {card_path}")

    # Mini card
    mini = generate_mini_card(report, args.theme)
    mini_path = output_dir / f'{safe_name}_mini.svg'
    mini_path.write_text(mini)
    if not args.quiet:
        print(f"Saved: {mini_path}")

    # JSON report
    if args.json:
        json_path = output_dir / f'{safe_name}_report.json'
        json_path.write_text(json.dumps(report, indent=2))
        if not args.quiet:
            print(f"Saved: {json_path}")

    if not args.quiet:
        print(f"\nTo embed in README:")
        print(f"  ![VSM Health]({badge_path})")


if __name__ == '__main__':
    main()
