"""
Contribute API Lambda
Handles user contributions to the dataset with rate limiting and classification.
"""

import json
import os
import hashlib
import math
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import boto3
from decimal import Decimal

import requests
from github import Github, Auth

# AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Environment
DATA_BUCKET = os.environ.get('DATA_BUCKET')
SUBMISSIONS_TABLE = os.environ.get('SUBMISSIONS_TABLE')
RATE_LIMITS_TABLE = os.environ.get('RATE_LIMITS_TABLE')

# Rate limit configuration
MAX_REPO_UPDATES_PER_DAY = 1
MAX_USER_SUBMISSIONS_PER_DAY = 10
MAX_TOTAL_DAILY_SUBMISSIONS = 100


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Handle contribution API requests.

    Endpoints:
    - POST /contribute - Submit a repo for classification
    - GET /contribute/{submissionId} - Check submission status
    """
    http_method = event.get('httpMethod', 'GET')
    path_params = event.get('pathParameters') or {}

    try:
        if http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            return submit_contribution(body)
        elif http_method == 'GET' and 'submissionId' in path_params:
            return get_submission_status(path_params['submissionId'])
        else:
            return response(404, {'error': 'Not found'})

    except Exception as e:
        print(f"Error: {e}")
        return response(500, {'error': str(e)})


def submit_contribution(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a contribution submission.

    Expected body:
    {
        "repo": "owner/repo",
        "github_token": "ghp_xxx",
        "user_hypothesis": "club",  // optional
        "consent_to_include": true
    }
    """
    # Validate required fields
    repo = body.get('repo', '').strip()
    token = body.get('github_token', '').strip()
    consent = body.get('consent_to_include', False)

    if not repo:
        return response(400, {'error': 'Repository is required'})
    if not token:
        return response(400, {'error': 'GitHub token is required'})
    if not consent:
        return response(400, {'error': 'Consent is required'})

    # Normalize repo format
    repo = normalize_repo(repo)
    if not repo:
        return response(400, {'error': 'Invalid repository format'})

    # Check rate limits
    rate_check = check_rate_limits(repo, token)
    if not rate_check['allowed']:
        return response(429, {
            'status': 'rate_limited',
            'message': rate_check['message'],
            'next_available': rate_check.get('next_available'),
        })

    # Generate submission ID
    submission_id = generate_submission_id(repo, token)

    # Record submission
    submissions_table = dynamodb.Table(SUBMISSIONS_TABLE)
    now = datetime.now(timezone.utc)

    submissions_table.put_item(Item={
        'pk': f'SUBMISSION#{submission_id}',
        'sk': 'STATUS',
        'submission_id': submission_id,
        'repo': repo,
        'user_hypothesis': body.get('user_hypothesis'),
        'status': 'processing',
        'created_at': now.isoformat(),
        'updated_at': now.isoformat(),
        'ttl': int((now + timedelta(days=30)).timestamp()),
    })

    # Update rate limits
    update_rate_limits(repo, token)

    # Collect and classify (synchronous for now, could be async)
    try:
        result = collect_and_classify(repo, token, body.get('user_hypothesis'))

        # Update submission with result
        submissions_table.update_item(
            Key={'pk': f'SUBMISSION#{submission_id}', 'sk': 'STATUS'},
            UpdateExpression='SET #status = :status, result = :result, updated_at = :now',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'completed',
                ':result': json.dumps(result, default=str),
                ':now': datetime.now(timezone.utc).isoformat(),
            }
        )

        # Save to contributions folder
        save_contribution(repo, result)

        return response(200, {
            'status': 'completed',
            'submission_id': submission_id,
            'result': result,
        })

    except Exception as e:
        # Update submission with error
        submissions_table.update_item(
            Key={'pk': f'SUBMISSION#{submission_id}', 'sk': 'STATUS'},
            UpdateExpression='SET #status = :status, error = :error, updated_at = :now',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'error',
                ':error': str(e),
                ':now': datetime.now(timezone.utc).isoformat(),
            }
        )

        return response(500, {
            'status': 'error',
            'submission_id': submission_id,
            'message': str(e),
        })


def get_submission_status(submission_id: str) -> Dict[str, Any]:
    """Get status of a submission."""
    submissions_table = dynamodb.Table(SUBMISSIONS_TABLE)

    result = submissions_table.get_item(
        Key={'pk': f'SUBMISSION#{submission_id}', 'sk': 'STATUS'}
    )

    if 'Item' not in result:
        return response(404, {'error': 'Submission not found'})

    item = result['Item']
    response_data = {
        'submission_id': item['submission_id'],
        'repo': item['repo'],
        'status': item['status'],
        'created_at': item['created_at'],
    }

    if item['status'] == 'completed' and 'result' in item:
        response_data['result'] = json.loads(item['result'])
    elif item['status'] == 'error' and 'error' in item:
        response_data['message'] = item['error']

    return response(200, response_data)


def normalize_repo(repo: str) -> Optional[str]:
    """Normalize repository input to owner/repo format."""
    import re

    # Remove common prefixes
    repo = repo.strip()
    repo = re.sub(r'^https?://(www\.)?github\.com/', '', repo)
    repo = re.sub(r'\.git$', '', repo)
    repo = repo.strip('/')

    # Validate format
    if re.match(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$', repo):
        return repo

    return None


def check_rate_limits(repo: str, token: str) -> Dict[str, Any]:
    """Check if request is within rate limits."""
    rate_table = dynamodb.Table(RATE_LIMITS_TABLE)
    now = datetime.now(timezone.utc)
    today = now.strftime('%Y-%m-%d')
    user_hash = hashlib.sha256(token.encode()).hexdigest()[:16]

    # Check repo rate limit (1 update per day)
    repo_key = f'REPO#{repo}#{today}'
    repo_limit = rate_table.get_item(Key={'pk': repo_key})
    if 'Item' in repo_limit:
        next_available = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0
        ).isoformat()
        return {
            'allowed': False,
            'message': 'This repository was already analyzed today',
            'next_available': next_available,
        }

    # Check user rate limit (10 per day)
    user_key = f'USER#{user_hash}#{today}'
    user_limit = rate_table.get_item(Key={'pk': user_key})
    user_count = int(user_limit.get('Item', {}).get('count', 0))
    if user_count >= MAX_USER_SUBMISSIONS_PER_DAY:
        return {
            'allowed': False,
            'message': f'You have reached the daily limit of {MAX_USER_SUBMISSIONS_PER_DAY} submissions',
        }

    # Check global rate limit
    global_key = f'GLOBAL#{today}'
    global_limit = rate_table.get_item(Key={'pk': global_key})
    global_count = int(global_limit.get('Item', {}).get('count', 0))
    if global_count >= MAX_TOTAL_DAILY_SUBMISSIONS:
        return {
            'allowed': False,
            'message': 'Daily submission limit reached. Please try again tomorrow.',
        }

    return {'allowed': True}


def update_rate_limits(repo: str, token: str) -> None:
    """Update rate limit counters."""
    rate_table = dynamodb.Table(RATE_LIMITS_TABLE)
    now = datetime.now(timezone.utc)
    today = now.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    ttl = int(tomorrow.timestamp()) + 86400  # Expire day after

    user_hash = hashlib.sha256(token.encode()).hexdigest()[:16]

    # Record repo usage
    rate_table.put_item(Item={
        'pk': f'REPO#{repo}#{today}',
        'count': 1,
        'ttl': ttl,
    })

    # Increment user counter
    rate_table.update_item(
        Key={'pk': f'USER#{user_hash}#{today}'},
        UpdateExpression='SET #count = if_not_exists(#count, :zero) + :one, #ttl = :ttl',
        ExpressionAttributeNames={'#count': 'count', '#ttl': 'ttl'},
        ExpressionAttributeValues={':zero': 0, ':one': 1, ':ttl': ttl},
    )

    # Increment global counter
    rate_table.update_item(
        Key={'pk': f'GLOBAL#{today}'},
        UpdateExpression='SET #count = if_not_exists(#count, :zero) + :one, #ttl = :ttl',
        ExpressionAttributeNames={'#count': 'count', '#ttl': 'ttl'},
        ExpressionAttributeValues={':zero': 0, ':one': 1, ':ttl': ttl},
    )


def generate_submission_id(repo: str, token: str) -> str:
    """Generate unique submission ID."""
    now = datetime.now(timezone.utc).isoformat()
    data = f'{repo}:{token}:{now}'
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def collect_and_classify(
    repo: str,
    token: str,
    user_hypothesis: Optional[str]
) -> Dict[str, Any]:
    """
    Collect data from GitHub and classify the repository.
    """
    auth = Auth.Token(token)
    github = Github(auth=auth)

    gh_repo = github.get_repo(repo)

    # Collect contributor data
    contributors = []
    for i, contrib in enumerate(gh_repo.get_contributors()):
        if i >= 100:
            break
        contributors.append({
            'login': contrib.login,
            'contributions': contrib.contributions,
        })

    # Calculate metrics
    contributions = [c['contributions'] for c in contributors]
    entropy = calculate_entropy(contributions)
    normalized_entropy = entropy / math.log2(len(contributors)) if len(contributors) > 1 else 0
    gini = calculate_gini(contributions)
    bus_factor = calculate_bus_factor(contributions)

    # Top contributor percentages
    total = sum(contributions)
    top1_pct = (contributions[0] / total * 100) if contributions else 0
    top5_pct = (sum(contributions[:5]) / total * 100) if len(contributions) >= 5 else top1_pct

    # Classify based on metrics
    predicted_category = classify_project(entropy, normalized_entropy, bus_factor, len(contributors))
    confidence = calculate_confidence(entropy, normalized_entropy, bus_factor, predicted_category)

    # Repository metrics
    metrics = {
        'repo': repo,
        'category': predicted_category,
        'confidence': confidence,
        'stars': gh_repo.stargazers_count,
        'forks': gh_repo.forks_count,
        'language': gh_repo.language,
        'total_contributors': len(contributors),
        'entropy': round(entropy, 4),
        'normalized_entropy': round(normalized_entropy, 4),
        'gini_coefficient': round(gini, 4),
        'bus_factor': bus_factor,
        'top1_percentage': round(top1_pct, 1),
        'top5_percentage': round(top5_pct, 1),
        'top_contributors': contributors[:10],
        'collected_at': datetime.now(timezone.utc).isoformat(),
    }

    # Check user hypothesis
    hypothesis_correct = None
    if user_hypothesis:
        hypothesis_correct = (user_hypothesis.lower() == predicted_category)

    return {
        'predicted_category': predicted_category,
        'confidence': confidence,
        'metrics': metrics,
        'user_hypothesis': user_hypothesis,
        'hypothesis_correct': hypothesis_correct,
    }


def calculate_entropy(contributions: List[int]) -> float:
    """Calculate Shannon entropy."""
    if not contributions:
        return 0

    total = sum(contributions)
    if total == 0:
        return 0

    entropy = 0
    for c in contributions:
        if c > 0:
            p = c / total
            entropy -= p * math.log2(p)

    return entropy


def calculate_gini(contributions: List[int]) -> float:
    """Calculate Gini coefficient."""
    if not contributions:
        return 0

    n = len(contributions)
    sorted_contribs = sorted(contributions)
    total = sum(contributions)

    if total == 0:
        return 0

    sum_of_diffs = 0
    for i in range(n):
        for j in range(n):
            sum_of_diffs += abs(sorted_contribs[i] - sorted_contribs[j])

    mean = total / n
    return sum_of_diffs / (2 * n * n * mean) if mean > 0 else 0


def calculate_bus_factor(contributions: List[int]) -> int:
    """Calculate bus factor (min contributors for 50% of work)."""
    if not contributions:
        return 0

    total = sum(contributions)
    threshold = total * 0.5
    sorted_contribs = sorted(contributions, reverse=True)

    cumsum = 0
    for i, c in enumerate(sorted_contribs, 1):
        cumsum += c
        if cumsum >= threshold:
            return i

    return len(contributions)


def classify_project(
    entropy: float,
    normalized_entropy: float,
    bus_factor: int,
    num_contributors: int
) -> str:
    """
    Classify project into governance category based on metrics.

    Thresholds (approximate):
    - Toy: normalized_entropy < 0.3, bus_factor <= 1
    - Stadium: normalized_entropy < 0.5, bus_factor <= 5
    - Club: normalized_entropy < 0.7, bus_factor <= 15
    - Federation: normalized_entropy >= 0.7 or bus_factor > 15
    """
    if bus_factor <= 1 and normalized_entropy < 0.4:
        return 'toy'
    elif bus_factor <= 5 and normalized_entropy < 0.5:
        return 'stadium'
    elif bus_factor <= 15 and normalized_entropy < 0.75:
        return 'club'
    else:
        return 'federation'


def calculate_confidence(
    entropy: float,
    normalized_entropy: float,
    bus_factor: int,
    predicted: str
) -> float:
    """Calculate confidence score for classification."""
    # Simple confidence based on how clearly the project falls into category
    if predicted == 'toy':
        conf = 0.9 if bus_factor == 1 else 0.7
    elif predicted == 'stadium':
        conf = 0.8 if normalized_entropy < 0.4 else 0.6
    elif predicted == 'club':
        conf = 0.75
    else:  # federation
        conf = 0.85 if bus_factor > 20 else 0.7

    return round(conf, 2)


def save_contribution(repo: str, result: Dict[str, Any]) -> None:
    """Save contribution to S3 for later incorporation."""
    key = f'contributions/{repo.replace("/", "_")}_{datetime.now(timezone.utc).strftime("%Y%m%d")}.json'

    s3.put_object(
        Bucket=DATA_BUCKET,
        Key=key,
        Body=json.dumps(result, indent=2, default=str),
        ContentType='application/json',
    )


def response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create API Gateway response."""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        },
        'body': json.dumps(body, default=str),
    }
