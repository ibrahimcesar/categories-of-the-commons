// Governance categories
export type GovernanceCategory = 'federation' | 'stadium' | 'club' | 'toy';

// Project data from collection
export interface ProjectData {
  repo: string;
  category: GovernanceCategory;
  collected_at: string;

  // Repository metrics
  stars: number;
  forks: number;
  open_issues: number;
  language: string;

  // Governance metrics
  entropy: number;
  normalized_entropy: number;
  gini_coefficient: number;
  bus_factor: number;
  top1_percentage: number;
  top5_percentage: number;

  // Contributors
  total_contributors: number;
  contributors: ContributorData[];

  // Governance files
  governance_files: GovernanceFiles;
}

export interface ContributorData {
  login: string;
  contributions: number;
  percentage: number;
}

export interface GovernanceFiles {
  'GOVERNANCE.md': boolean;
  'CONTRIBUTING.md': boolean;
  'CODE_OF_CONDUCT.md': boolean;
  'SECURITY.md': boolean;
  'MAINTAINERS.md': boolean;
  '.github/CODEOWNERS': boolean;
}

// Category statistics
export interface CategoryStats {
  category: GovernanceCategory;
  count: number;
  avg_entropy: number;
  std_entropy: number;
  avg_bus_factor: number;
  avg_contributors: number;
}

// Dataset summary
export interface DatasetSummary {
  total_projects: number;
  categories: CategoryStats[];
  last_updated: string;
}

// Contribution request
export interface ContributionRequest {
  repo: string;
  github_token: string;
  user_hypothesis?: GovernanceCategory;
  consent_to_include: boolean;
}

// Contribution response
export interface ContributionResponse {
  status: 'queued' | 'processing' | 'completed' | 'error' | 'rate_limited';
  message: string;

  // If completed
  result?: {
    predicted_category: GovernanceCategory;
    confidence: number;
    metrics: ProjectData;
    comparison: CategoryComparison;
  };

  // If rate limited
  next_available?: string;
}

// Comparison with dataset
export interface CategoryComparison {
  category: GovernanceCategory;
  percentile_entropy: number;
  percentile_bus_factor: number;
  similar_projects: string[];
}

// API responses
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
