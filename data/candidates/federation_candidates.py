"""
Federation Project Candidates
Distributed governance, multiple organizations, formal structure.
"""

# Candidates to collect
CANDIDATES = [
    # Linux Foundation projects
    "kubernetes/kubernetes",
    "nodejs/node",
    "prometheus/prometheus",
    "grafana/grafana",

    # Apache Foundation
    "apache/kafka",
    "apache/spark",
    "apache/hadoop",
    "apache/airflow",

    # CNCF projects
    "envoyproxy/envoy",
    "containerd/containerd",
    "etcd-io/etcd",
    "helm/helm",

    # Mozilla
    "nicotine-plus/nicotine-plus",  # Example community project

    # Python/PSF
    "python/cpython",
    "django/django",

    # Rust Foundation
    "rust-lang/rust",

    # Other foundations
    "eclipse/che",
    "openstack/nova",

    # Linux Foundation - OpenTofu
    # Forked from Terraform after HashiCorp BSL license change (2023)
    # Interesting case study: rapid community mobilization, fork governance
    "opentofu/opentofu",
]

# High priority for collection
HIGH_PRIORITY = [
    "kubernetes/kubernetes",
    "nodejs/node",
    "python/cpython",
    "rust-lang/rust",
    "apache/kafka",
    "opentofu/opentofu",  # Fork governance case study
]

# Already collected (if any)
COLLECTED = []
