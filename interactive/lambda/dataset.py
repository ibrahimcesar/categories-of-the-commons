"""
Dataset API Lambda
Serves aggregated dataset information and project details.
"""

import json
import os
import boto3
from typing import Any, Dict

s3 = boto3.client('s3')
DATA_BUCKET = os.environ.get('DATA_BUCKET')


def handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    Handle dataset API requests.

    Endpoints:
    - GET /dataset - Returns dataset summary and all projects
    - GET /dataset/project/{projectId} - Returns specific project data
    """
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '')
    path_params = event.get('pathParameters') or {}

    try:
        if path == '/dataset' or path == '/v1/dataset':
            return get_dataset_summary()
        elif 'projectId' in path_params:
            project_id = path_params['projectId']
            return get_project(project_id)
        else:
            return response(404, {'error': 'Not found'})

    except Exception as e:
        print(f"Error: {e}")
        return response(500, {'error': str(e)})


def get_dataset_summary() -> Dict[str, Any]:
    """Get summary of the entire dataset."""
    try:
        # List all processed metric files
        result = s3.list_objects_v2(
            Bucket=DATA_BUCKET,
            Prefix='processed/'
        )

        # Load summary if exists
        try:
            summary_obj = s3.get_object(
                Bucket=DATA_BUCKET,
                Key='processed/summary.json'
            )
            summary = json.loads(summary_obj['Body'].read().decode('utf-8'))
        except s3.exceptions.NoSuchKey:
            # Generate basic summary from raw files
            summary = generate_summary()

        return response(200, summary)

    except Exception as e:
        return response(500, {'error': f'Failed to load dataset: {str(e)}'})


def get_project(project_id: str) -> Dict[str, Any]:
    """Get data for a specific project."""
    # Project ID format: owner_repo (converted from owner/repo)
    try:
        # Try processed metrics first
        key = f'processed/{project_id}_metrics.json'
        try:
            obj = s3.get_object(Bucket=DATA_BUCKET, Key=key)
            data = json.loads(obj['Body'].read().decode('utf-8'))
            return response(200, data)
        except s3.exceptions.NoSuchKey:
            pass

        # Fall back to raw data
        key = f'raw/{project_id}_data.json'
        obj = s3.get_object(Bucket=DATA_BUCKET, Key=key)
        data = json.loads(obj['Body'].read().decode('utf-8'))
        return response(200, data)

    except s3.exceptions.NoSuchKey:
        return response(404, {'error': f'Project not found: {project_id}'})
    except Exception as e:
        return response(500, {'error': str(e)})


def generate_summary() -> Dict[str, Any]:
    """Generate summary from raw data files."""
    projects = []
    category_counts = {'federation': 0, 'stadium': 0, 'club': 0, 'toy': 0}

    # List raw files
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=DATA_BUCKET, Prefix='raw/'):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('_data.json'):
                key = obj['Key']
                project_id = key.replace('raw/', '').replace('_data.json', '')
                projects.append({
                    'id': project_id,
                    'key': key,
                    'last_modified': obj['LastModified'].isoformat(),
                })

    return {
        'total_projects': len(projects),
        'categories': category_counts,
        'projects': projects[:100],  # Limit for initial load
        'has_more': len(projects) > 100,
    }


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
