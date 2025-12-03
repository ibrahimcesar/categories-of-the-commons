import { useParams, Link } from 'react-router-dom'
import {
  Star,
  GitFork,
  Users,
  Calendar,
  ExternalLink,
  FileText,
  ArrowLeft,
} from 'lucide-react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import CategoryBadge from '../components/CategoryBadge'
import type { GovernanceCategory } from '../types'

// Mock data - will be replaced with API call
const mockProject = {
  repo: 'neovim/neovim',
  category: 'club' as GovernanceCategory,
  description: 'Vim-fork focused on extensibility and usability',
  language: 'C',
  stars: 75000,
  forks: 5200,
  open_issues: 1800,
  collected_at: '2024-12-01',

  // Metrics
  entropy: 2.85,
  normalized_entropy: 0.68,
  gini_coefficient: 0.72,
  bus_factor: 12,
  top1_percentage: 28,
  top5_percentage: 58,

  // Contributors
  total_contributors: 1200,
  top_contributors: [
    { login: 'justinmk', contributions: 4500, percentage: 28 },
    { login: 'bfredl', contributions: 2100, percentage: 13 },
    { login: 'ZyX-I', contributions: 1800, percentage: 11 },
    { login: 'fwalch', contributions: 850, percentage: 5 },
    { login: 'equalsraf', contributions: 620, percentage: 4 },
  ],

  // Governance files
  governance_files: {
    'GOVERNANCE.md': false,
    'CONTRIBUTING.md': true,
    'CODE_OF_CONDUCT.md': true,
    'SECURITY.md': true,
    'MAINTAINERS.md': false,
    '.github/CODEOWNERS': true,
  },
}

const COLORS = ['#58a6ff', '#3fb950', '#d29922', '#a371f7', '#8b949e']

export default function ProjectPage() {
  const { owner, repo } = useParams()
  const fullRepo = `${owner}/${repo}`

  // In real app, fetch project data here
  const project = mockProject

  const contributorData = project.top_contributors.map((c) => ({
    name: c.login,
    value: c.contributions,
  }))

  const governanceFiles = Object.entries(project.governance_files)

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        to="/explore"
        className="inline-flex items-center gap-2 text-sm hover:text-[var(--color-accent-fg)] transition-colors"
        style={{ color: 'var(--color-fg-muted)' }}
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Explore
      </Link>

      {/* Header */}
      <div className="card p-6">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-2xl font-bold">{fullRepo}</h1>
              <CategoryBadge category={project.category} size="md" />
            </div>
            <p style={{ color: 'var(--color-fg-muted)' }}>{project.description}</p>
          </div>
          <a
            href={`https://github.com/${fullRepo}`}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-secondary"
          >
            <ExternalLink className="w-4 h-4" />
            View on GitHub
          </a>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6">
          <div className="flex items-center gap-2">
            <Star className="w-5 h-5" style={{ color: 'var(--color-attention-fg)' }} />
            <div>
              <div className="font-semibold">{project.stars.toLocaleString()}</div>
              <div className="text-xs" style={{ color: 'var(--color-fg-muted)' }}>Stars</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <GitFork className="w-5 h-5" style={{ color: 'var(--color-fg-muted)' }} />
            <div>
              <div className="font-semibold">{project.forks.toLocaleString()}</div>
              <div className="text-xs" style={{ color: 'var(--color-fg-muted)' }}>Forks</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Users className="w-5 h-5" style={{ color: 'var(--color-success-fg)' }} />
            <div>
              <div className="font-semibold">{project.total_contributors.toLocaleString()}</div>
              <div className="text-xs" style={{ color: 'var(--color-fg-muted)' }}>Contributors</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div
              className="w-5 h-5 rounded-full"
              style={{ backgroundColor: '#555a63' }}
            />
            <div>
              <div className="font-semibold">{project.language}</div>
              <div className="text-xs" style={{ color: 'var(--color-fg-muted)' }}>Language</div>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Calendar className="w-5 h-5" style={{ color: 'var(--color-fg-muted)' }} />
            <div>
              <div className="font-semibold">{project.collected_at}</div>
              <div className="text-xs" style={{ color: 'var(--color-fg-muted)' }}>Collected</div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Governance Metrics */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4">Governance Metrics</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Shannon Entropy</span>
              <span className="font-mono font-semibold">{project.entropy.toFixed(3)} bits</span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Normalized Entropy</span>
              <span className="font-mono font-semibold">{project.normalized_entropy.toFixed(3)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Gini Coefficient</span>
              <span className="font-mono font-semibold">{project.gini_coefficient.toFixed(3)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Bus Factor</span>
              <span className="font-mono font-semibold">{project.bus_factor}</span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Top 1 Contributor</span>
              <span className="font-mono font-semibold">{project.top1_percentage}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span style={{ color: 'var(--color-fg-muted)' }}>Top 5 Contributors</span>
              <span className="font-mono font-semibold">{project.top5_percentage}%</span>
            </div>
          </div>
        </div>

        {/* Governance Files */}
        <div className="card p-6">
          <h2 className="text-lg font-semibold mb-4">Governance Files</h2>
          <div className="space-y-2">
            {governanceFiles.map(([file, present]) => (
              <div key={file} className="flex items-center gap-2">
                <FileText
                  className="w-4 h-4"
                  style={{ color: present ? 'var(--color-success-fg)' : 'var(--color-fg-subtle)' }}
                />
                <span className={present ? '' : 'opacity-50'}>{file}</span>
                <span
                  className="ml-auto text-xs px-2 py-0.5 rounded"
                  style={{
                    backgroundColor: present ? 'rgba(63, 185, 80, 0.2)' : 'rgba(139, 148, 158, 0.2)',
                    color: present ? 'var(--color-success-fg)' : 'var(--color-fg-subtle)',
                  }}
                >
                  {present ? 'Present' : 'Missing'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Contributors */}
      <div className="card p-6">
        <h2 className="text-lg font-semibold mb-4">Top Contributors</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {/* Bar chart */}
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={project.top_contributors}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-muted)" />
                <XAxis type="number" tick={{ fill: 'var(--color-fg-muted)' }} />
                <YAxis
                  type="category"
                  dataKey="login"
                  tick={{ fill: 'var(--color-fg-muted)' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--color-canvas-subtle)',
                    border: '1px solid var(--color-border-default)',
                    borderRadius: '6px',
                  }}
                />
                <Bar dataKey="contributions" fill="var(--color-accent-fg)" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Pie chart */}
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={contributorData}
                  cx="50%"
                  cy="50%"
                  innerRadius={40}
                  outerRadius={80}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                  labelLine={{ stroke: 'var(--color-fg-muted)' }}
                >
                  {contributorData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--color-canvas-subtle)',
                    border: '1px solid var(--color-border-default)',
                    borderRadius: '6px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Contributor list */}
        <div className="mt-6">
          <table className="table">
            <thead>
              <tr>
                <th>Contributor</th>
                <th className="text-right">Contributions</th>
                <th className="text-right">Percentage</th>
              </tr>
            </thead>
            <tbody>
              {project.top_contributors.map((c) => (
                <tr key={c.login}>
                  <td>
                    <a
                      href={`https://github.com/${c.login}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 hover:text-[var(--color-accent-fg)]"
                    >
                      <img
                        src={`https://github.com/${c.login}.png?size=32`}
                        alt={c.login}
                        className="w-6 h-6 rounded-full"
                      />
                      {c.login}
                    </a>
                  </td>
                  <td className="text-right font-mono">{c.contributions.toLocaleString()}</td>
                  <td className="text-right font-mono">{c.percentage}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
