"""
VSM Health Badge API Service

A FastAPI service that generates dynamic VSM health badges for OSS projects.
Can be deployed to Vercel, Railway, Render, or any Python host.

Endpoints:
- GET /badge/{owner}/{repo} - Simple shield badge
- GET /card/{owner}/{repo} - Detailed health card
- GET /mini/{owner}/{repo} - Compact mini card
- GET /report/{owner}/{repo} - JSON health report
- GET /health - Service health check

Usage:
    uvicorn api.main:app --reload

Deploy to Vercel:
    vercel --prod
"""

import os
import json
import math
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

# Initialize FastAPI app
app = FastAPI(
    title="VSM Health Badge API",
    description="Generate dynamic VSM (Viable System Model) health badges for OSS projects",
    version="1.0.0",
)

# CORS middleware for embedding badges
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Cache for GitHub data (simple in-memory cache)
_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = timedelta(hours=1)

# GitHub API token (optional, increases rate limits)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# =============================================================================
# GitHub Data Fetcher
# =============================================================================

async def fetch_github_data(owner: str, repo: str) -> Dict[str, Any]:
    """Fetch project data from GitHub API."""
    cache_key = f"{owner}/{repo}"

    # Check cache
    if cache_key in _cache:
        cached = _cache[cache_key]
        if datetime.now() - cached["timestamp"] < CACHE_TTL:
            return cached["data"]

    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    async with httpx.AsyncClient() as client:
        try:
            # Fetch repository info
            repo_resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=headers,
                timeout=10.0
            )
            if repo_resp.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Repository {owner}/{repo} not found")
            repo_resp.raise_for_status()
            repo_data = repo_resp.json()

            # Fetch contributors (top 30)
            contributors_resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/contributors",
                headers=headers,
                params={"per_page": 30},
                timeout=10.0
            )
            contributors = contributors_resp.json() if contributors_resp.status_code == 200 else []

            # Fetch recent commits
            commits_resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits",
                headers=headers,
                params={"per_page": 50},
                timeout=10.0
            )
            commits = commits_resp.json() if commits_resp.status_code == 200 else []

            # Fetch open pull requests
            prs_resp = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/pulls",
                headers=headers,
                params={"state": "all", "per_page": 30},
                timeout=10.0
            )
            prs = prs_resp.json() if prs_resp.status_code == 200 else []

            # Check for governance files
            governance_files = {}
            files_to_check = [
                "GOVERNANCE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md",
                "MAINTAINERS.md", ".github/CODEOWNERS", "ROADMAP.md"
            ]
            for file_path in files_to_check:
                file_resp = await client.get(
                    f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}",
                    headers=headers,
                    timeout=5.0
                )
                governance_files[file_path] = file_resp.status_code == 200

            data = {
                "repository": repo_data,
                "contributors": contributors if isinstance(contributors, list) else [],
                "recent_commits": commits if isinstance(commits, list) else [],
                "pull_requests": prs if isinstance(prs, list) else [],
                "governance_files": governance_files,
            }

            # Cache the result
            _cache[cache_key] = {"data": data, "timestamp": datetime.now()}

            return data

        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"GitHub API error: {str(e)}")


# =============================================================================
# VSM Health Calculator
# =============================================================================

class VSMHealthCalculator:
    """Calculate VSM health scores from GitHub data."""

    COLORS = {
        'healthy': '#2ecc71',
        'warning': '#f39c12',
        'critical': '#e74c3c',
    }

    RISK_COLORS = {
        'LOW': '#2ecc71',
        'MEDIUM': '#f1c40f',
        'HIGH': '#e67e22',
        'CRITICAL': '#e74c3c',
    }

    @staticmethod
    def get_score_color(score: float) -> str:
        if score >= 70:
            return VSMHealthCalculator.COLORS['healthy']
        elif score >= 40:
            return VSMHealthCalculator.COLORS['warning']
        return VSMHealthCalculator.COLORS['critical']

    @staticmethod
    def get_status(score: float) -> str:
        if score >= 70:
            return 'healthy'
        elif score >= 40:
            return 'warning'
        return 'critical'

    def calculate_bus_factor(self, contributors: list) -> int:
        """Calculate bus factor from contributor list."""
        if not contributors:
            return 0

        contributions = sorted(
            [c.get('contributions', 0) for c in contributors],
            reverse=True
        )
        total = sum(contributions)
        if total == 0:
            return 0

        cumsum = 0
        bus_factor = 0
        for c in contributions:
            cumsum += c
            bus_factor += 1
            if cumsum >= total * 0.5:
                break
        return bus_factor

    def analyze_s1(self, data: Dict) -> Dict:
        """S1: Operations - Primary activities."""
        contributors = data.get('contributors', [])
        commits = data.get('recent_commits', [])
        prs = data.get('pull_requests', [])

        contributor_count = len(contributors)
        commit_count = len(commits)
        pr_count = len(prs)
        bus_factor = self.calculate_bus_factor(contributors)

        score = 0
        score += min(30, contributor_count * 0.5)
        score += min(25, commit_count * 0.5)
        score += min(25, pr_count * 0.5)
        score += min(20, bus_factor * 5)

        return {
            'score': min(100, score),
            'status': self.get_status(score),
            'indicators': {
                'contributors': contributor_count,
                'commits': commit_count,
                'prs': pr_count,
                'bus_factor': bus_factor,
            }
        }

    def analyze_s2(self, data: Dict) -> Dict:
        """S2: Coordination - Review processes."""
        gov_files = data.get('governance_files', {})
        prs = data.get('pull_requests', [])

        has_codeowners = gov_files.get('.github/CODEOWNERS', False)

        # Estimate review rate from PRs
        if prs:
            # Check if PRs have reviews (simplified check)
            reviewed = sum(1 for pr in prs if pr.get('requested_reviewers'))
            review_rate = reviewed / len(prs)
        else:
            review_rate = 0

        score = 0
        score += 30 if has_codeowners else 0
        score += review_rate * 40
        score += 30 if len(prs) > 0 else 0  # Has PR activity

        return {
            'score': min(100, score),
            'status': self.get_status(score),
            'indicators': {
                'has_codeowners': has_codeowners,
                'review_rate': f"{review_rate:.0%}",
            }
        }

    def analyze_s3(self, data: Dict) -> Dict:
        """S3: Control - Internal regulation."""
        gov_files = data.get('governance_files', {})
        contributors = data.get('contributors', [])

        has_contributing = gov_files.get('CONTRIBUTING.md', False)
        has_maintainers = gov_files.get('MAINTAINERS.md', False)

        # Estimate active maintainers from top contributors
        active_maintainers = min(5, len([c for c in contributors[:10] if c.get('contributions', 0) > 10]))

        score = 0
        score += 25 if has_contributing else 0
        score += 25 if has_maintainers else 0
        score += min(50, active_maintainers * 12.5)

        return {
            'score': min(100, score),
            'status': self.get_status(score),
            'indicators': {
                'has_contributing': has_contributing,
                'has_maintainers': has_maintainers,
                'active_maintainers': active_maintainers,
            }
        }

    def analyze_s4(self, data: Dict) -> Dict:
        """S4: Intelligence - Environment scanning."""
        repo = data.get('repository', {})
        gov_files = data.get('governance_files', {})

        has_discussions = repo.get('has_discussions', False)
        has_roadmap = gov_files.get('ROADMAP.md', False)
        has_wiki = repo.get('has_wiki', False)

        score = 0
        score += 30 if has_discussions else 0
        score += 30 if has_roadmap else 0
        score += 20 if has_wiki else 0
        score += 20 if repo.get('open_issues_count', 0) > 0 else 0  # Active issues

        return {
            'score': min(100, score),
            'status': self.get_status(score),
            'indicators': {
                'has_discussions': has_discussions,
                'has_roadmap': has_roadmap,
                'has_wiki': has_wiki,
            }
        }

    def analyze_s5(self, data: Dict) -> Dict:
        """S5: Policy - Identity and governance."""
        repo = data.get('repository', {})
        gov_files = data.get('governance_files', {})

        has_governance = gov_files.get('GOVERNANCE.md', False)
        has_coc = gov_files.get('CODE_OF_CONDUCT.md', False)
        has_license = repo.get('license') is not None
        has_description = bool(repo.get('description'))

        # Check for foundation backing
        owner = repo.get('owner', {}).get('login', '').lower()
        foundation_indicators = ['apache', 'linux', 'cncf', 'eclipse', 'python', 'rust-lang']
        is_foundation = any(f in owner for f in foundation_indicators)

        score = 0
        score += 30 if has_governance else 0
        score += 20 if has_coc else 0
        score += 20 if has_license else 0
        score += 10 if has_description else 0
        score += 20 if is_foundation else 0

        return {
            'score': min(100, score),
            'status': self.get_status(score),
            'indicators': {
                'has_governance': has_governance,
                'has_coc': has_coc,
                'has_license': has_license,
                'is_foundation': is_foundation,
            }
        }

    def generate_report(self, data: Dict) -> Dict:
        """Generate complete VSM health report."""
        repo = data.get('repository', {})

        subsystems = {
            'S1': self.analyze_s1(data),
            'S2': self.analyze_s2(data),
            'S3': self.analyze_s3(data),
            'S4': self.analyze_s4(data),
            'S5': self.analyze_s5(data),
        }

        # Weighted overall score
        weights = {'S1': 0.25, 'S2': 0.20, 'S3': 0.20, 'S4': 0.15, 'S5': 0.20}
        overall_score = sum(subsystems[k]['score'] * weights[k] for k in subsystems)

        # Risk level
        critical_count = sum(1 for s in subsystems.values() if s['status'] == 'critical')
        if critical_count >= 2 or overall_score < 30:
            risk_level = 'CRITICAL'
        elif critical_count >= 1 or overall_score < 50:
            risk_level = 'HIGH'
        elif overall_score < 70:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        # Determine category (simplified heuristic)
        stars = repo.get('stargazers_count', 0)
        contributors_count = len(data.get('contributors', []))

        if overall_score >= 60 and contributors_count > 50:
            category = 'federation'
        elif overall_score >= 45 and contributors_count > 20:
            category = 'club'
        elif contributors_count > 5:
            category = 'stadium'
        else:
            category = 'toy'

        return {
            'repository': repo.get('full_name', ''),
            'overall_score': overall_score,
            'risk_level': risk_level,
            'category': category,
            'subsystems': subsystems,
            'generated_at': datetime.now().isoformat(),
        }


# =============================================================================
# SVG Badge Generators
# =============================================================================

class BadgeGenerator:
    """Generate SVG badges from health reports."""

    COLORS = VSMHealthCalculator.COLORS
    RISK_COLORS = VSMHealthCalculator.RISK_COLORS

    @staticmethod
    def get_score_color(score: float) -> str:
        return VSMHealthCalculator.get_score_color(score)

    def generate_simple_badge(self, report: Dict) -> str:
        """Generate shields.io style badge."""
        score = int(report['overall_score'])
        color = self.get_score_color(report['overall_score'])

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

    def generate_detailed_card(self, report: Dict, theme: str = 'dark') -> str:
        """Generate detailed health card."""
        width = 400
        height = 280
        padding = 20

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
        subsystem_names = ['Operations', 'Coordination', 'Control', 'Intelligence', 'Policy']

        score_color = self.get_score_color(report['overall_score'])
        risk_color = self.RISK_COLORS.get(report['risk_level'], '#888')

        bars_svg = ""
        bar_y_start = 100
        bar_height = 8
        bar_spacing = 30
        bar_width = width - 2 * padding - 120

        for i, (sys_key, sys_name) in enumerate(zip(subsystems, subsystem_names)):
            sub = report['subsystems'][sys_key]
            y = bar_y_start + i * bar_spacing
            filled_width = (sub['score'] / 100) * bar_width
            bar_color = self.get_score_color(sub['score'])

            bars_svg += f'''
    <text x="{padding}" y="{y + 6}" font-size="12" fill="{text_color}">{sys_key}: {sys_name}</text>
    <rect x="{padding + 120}" y="{y - 4}" width="{bar_width}" height="{bar_height}" rx="4" fill="{border_color}"/>
    <rect x="{padding + 120}" y="{y - 4}" width="{filled_width}" height="{bar_height}" rx="4" fill="{bar_color}"/>
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
  <text x="{width - padding}" y="{height - 15}" font-family="Segoe UI, Ubuntu, sans-serif" font-size="9" fill="{text_secondary}" text-anchor="end">vsm-health.dev</text>
</svg>'''

    def generate_mini_card(self, report: Dict, theme: str = 'dark') -> str:
        """Generate compact mini card with radar."""
        width = 250
        height = 80

        if theme == 'dark':
            bg_color = '#1a1a2e'
            text_color = '#ffffff'
            text_secondary = '#a0a0a0'
            border_color = '#333355'
        else:
            bg_color = '#ffffff'
            text_color = '#333333'
            text_secondary = '#666666'
            border_color = '#e1e4e8'

        score_color = self.get_score_color(report['overall_score'])

        # Mini radar points
        subsystems = ['S1', 'S2', 'S3', 'S4', 'S5']
        scores = [report['subsystems'][s]['score'] for s in subsystems]

        cx, cy = 45, 45
        r = 25
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


# Initialize services
calculator = VSMHealthCalculator()
badge_generator = BadgeGenerator()


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/")
async def root():
    """API root - documentation."""
    return {
        "name": "VSM Health Badge API",
        "version": "1.0.0",
        "endpoints": {
            "badge": "/badge/{owner}/{repo}",
            "card": "/card/{owner}/{repo}?theme=dark|light",
            "mini": "/mini/{owner}/{repo}?theme=dark|light",
            "report": "/report/{owner}/{repo}",
            "health": "/health",
        },
        "example": {
            "badge": "/badge/curl/curl",
            "card": "/card/grafana/grafana?theme=dark",
        }
    }


@app.get("/health")
async def health_check():
    """Service health check."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/badge/{owner}/{repo}")
async def get_badge(owner: str, repo: str):
    """Generate simple shield badge."""
    data = await fetch_github_data(owner, repo)
    report = calculator.generate_report(data)
    svg = badge_generator.generate_simple_badge(report)

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
            "ETag": f'"{owner}/{repo}-{int(report["overall_score"])}"',
        }
    )


@app.get("/card/{owner}/{repo}")
async def get_card(
    owner: str,
    repo: str,
    theme: str = Query(default="dark", regex="^(dark|light)$")
):
    """Generate detailed health card."""
    data = await fetch_github_data(owner, repo)
    report = calculator.generate_report(data)
    svg = badge_generator.generate_detailed_card(report, theme)

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
        }
    )


@app.get("/mini/{owner}/{repo}")
async def get_mini(
    owner: str,
    repo: str,
    theme: str = Query(default="dark", regex="^(dark|light)$")
):
    """Generate mini card with radar."""
    data = await fetch_github_data(owner, repo)
    report = calculator.generate_report(data)
    svg = badge_generator.generate_mini_card(report, theme)

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={
            "Cache-Control": "public, max-age=3600",
        }
    )


@app.get("/report/{owner}/{repo}")
async def get_report(owner: str, repo: str):
    """Get full JSON health report."""
    data = await fetch_github_data(owner, repo)
    report = calculator.generate_report(data)
    return JSONResponse(content=report)


# =============================================================================
# Vercel Serverless Handler
# =============================================================================

# For Vercel deployment, the app is exported as 'app'
# Create vercel.json with: {"builds": [{"src": "api/main.py", "use": "@vercel/python"}]}
