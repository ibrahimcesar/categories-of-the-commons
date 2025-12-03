import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Search, Star, GitFork, Users, ExternalLink, SlidersHorizontal } from 'lucide-react'
import CategoryBadge from '../components/CategoryBadge'
import type { GovernanceCategory } from '../types'

// Mock data - will be replaced with API call
const mockProjects = [
  { repo: 'kubernetes/kubernetes', category: 'federation' as const, stars: 105000, contributors: 3500, entropy: 4.2, bus_factor: 45 },
  { repo: 'nodejs/node', category: 'federation' as const, stars: 102000, contributors: 3200, entropy: 3.9, bus_factor: 38 },
  { repo: 'curl/curl', category: 'stadium' as const, stars: 33000, contributors: 890, entropy: 1.8, bus_factor: 3 },
  { repo: 'neovim/neovim', category: 'club' as const, stars: 75000, contributors: 1200, entropy: 2.8, bus_factor: 12 },
  { repo: 'pallets/flask', category: 'club' as const, stars: 65000, contributors: 680, entropy: 2.5, bus_factor: 8 },
  { repo: 'sindresorhus/is-odd', category: 'toy' as const, stars: 450, contributors: 12, entropy: 0.8, bus_factor: 1 },
  { repo: 'BurntSushi/ripgrep', category: 'toy' as const, stars: 42000, contributors: 380, entropy: 1.2, bus_factor: 1 },
  { repo: 'grafana/grafana', category: 'federation' as const, stars: 59000, contributors: 2100, entropy: 3.5, bus_factor: 28 },
  { repo: 'axios/axios', category: 'stadium' as const, stars: 103000, contributors: 420, entropy: 1.5, bus_factor: 4 },
  { repo: 'lodash/lodash', category: 'stadium' as const, stars: 58000, contributors: 320, entropy: 1.3, bus_factor: 2 },
]

const categories: (GovernanceCategory | 'all')[] = ['all', 'federation', 'stadium', 'club', 'toy']

export default function ExplorePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState<'stars' | 'entropy' | 'contributors'>('stars')

  const categoryFilter = (searchParams.get('category') || 'all') as GovernanceCategory | 'all'

  const filteredProjects = useMemo(() => {
    let result = [...mockProjects]

    // Filter by category
    if (categoryFilter !== 'all') {
      result = result.filter((p) => p.category === categoryFilter)
    }

    // Filter by search
    if (search) {
      const searchLower = search.toLowerCase()
      result = result.filter((p) => p.repo.toLowerCase().includes(searchLower))
    }

    // Sort
    result.sort((a, b) => b[sortBy] - a[sortBy])

    return result
  }, [categoryFilter, search, sortBy])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold">Explore Dataset</h1>
        <p className="mt-1" style={{ color: 'var(--color-fg-muted)' }}>
          Browse and filter {mockProjects.length} projects across governance categories
        </p>
      </div>

      {/* Filters */}
      <div className="card p-4">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="relative flex-1">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4"
              style={{ color: 'var(--color-fg-subtle)' }}
            />
            <input
              type="text"
              placeholder="Search projects..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input pl-10"
            />
          </div>

          {/* Category filter */}
          <div className="flex gap-2 flex-wrap">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => {
                  if (cat === 'all') {
                    searchParams.delete('category')
                  } else {
                    searchParams.set('category', cat)
                  }
                  setSearchParams(searchParams)
                }}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  categoryFilter === cat
                    ? 'bg-[var(--color-accent-emphasis)] text-white'
                    : 'bg-[var(--color-canvas-inset)] hover:bg-[var(--color-border-muted)]'
                }`}
              >
                {cat === 'all' ? 'All' : cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>

          {/* Sort */}
          <div className="flex items-center gap-2">
            <SlidersHorizontal className="w-4 h-4" style={{ color: 'var(--color-fg-subtle)' }} />
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as typeof sortBy)}
              className="input w-auto"
            >
              <option value="stars">Stars</option>
              <option value="entropy">Entropy</option>
              <option value="contributors">Contributors</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results count */}
      <p className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>
        Showing {filteredProjects.length} projects
      </p>

      {/* Project list */}
      <div className="space-y-2">
        {filteredProjects.map((project) => (
          <Link
            key={project.repo}
            to={`/project/${project.repo}`}
            className="card p-4 flex items-center gap-4 hover:border-[var(--color-border-default)] transition-colors group"
          >
            {/* Repo icon */}
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
              style={{ backgroundColor: 'var(--color-canvas-inset)' }}
            >
              <GitFork className="w-5 h-5" style={{ color: 'var(--color-fg-muted)' }} />
            </div>

            {/* Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                <h3 className="font-semibold truncate group-hover:text-[var(--color-accent-fg)] transition-colors">
                  {project.repo}
                </h3>
                <CategoryBadge category={project.category} size="sm" />
              </div>
              <div className="flex items-center gap-4 mt-1 text-sm" style={{ color: 'var(--color-fg-muted)' }}>
                <span className="flex items-center gap-1">
                  <Star className="w-4 h-4" />
                  {project.stars.toLocaleString()}
                </span>
                <span className="flex items-center gap-1">
                  <Users className="w-4 h-4" />
                  {project.contributors.toLocaleString()}
                </span>
                <span>
                  Entropy: {project.entropy.toFixed(2)}
                </span>
                <span>
                  Bus Factor: {project.bus_factor}
                </span>
              </div>
            </div>

            {/* External link */}
            <a
              href={`https://github.com/${project.repo}`}
              target="_blank"
              rel="noopener noreferrer"
              onClick={(e) => e.stopPropagation()}
              className="p-2 rounded hover:bg-[var(--color-canvas-inset)] transition-colors"
            >
              <ExternalLink className="w-4 h-4" style={{ color: 'var(--color-fg-muted)' }} />
            </a>
          </Link>
        ))}
      </div>
    </div>
  )
}
