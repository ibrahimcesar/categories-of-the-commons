import { Link } from 'react-router-dom'
import {
  Search,
  Calculator,
  GitCompare,
  Plus,
  ArrowRight,
  Users,
  GitFork,
  Star,
  Activity
} from 'lucide-react'
import { CategoryCard } from '../components/CategoryBadge'

// Mock data - will be replaced with API call
const mockStats = {
  total_projects: 91,
  total_contributors: 15420,
  categories: {
    federation: 19,
    stadium: 37,
    club: 19,
    toy: 16,
  }
}

const features = [
  {
    name: 'Explore Dataset',
    description: 'Browse all collected projects, filter by category, and view detailed metrics.',
    href: '/explore',
    icon: Search,
  },
  {
    name: 'Interactive Equations',
    description: 'Understand the math behind governance metrics with live calculations.',
    href: '/equations',
    icon: Calculator,
  },
  {
    name: 'Compare Projects',
    description: 'See how projects compare across categories and metrics.',
    href: '/compare',
    icon: GitCompare,
  },
  {
    name: 'Contribute Data',
    description: 'Add your own GitHub repos to the dataset and see how they classify.',
    href: '/contribute',
    icon: Plus,
  },
]

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero */}
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold mb-4">
          Categories of the Commons
        </h1>
        <p
          className="text-xl max-w-2xl mx-auto mb-8"
          style={{ color: 'var(--color-fg-muted)' }}
        >
          Exploring open source governance patterns through the lens of commons theory.
          Quantitative analysis of contributor dynamics across different governance models.
        </p>

        <div className="flex justify-center gap-4">
          <Link to="/explore" className="btn btn-primary">
            Explore Dataset
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link to="/contribute" className="btn btn-secondary">
            Contribute
            <Plus className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="card p-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="stat-value flex items-center justify-center gap-2">
              <Activity className="w-6 h-6" style={{ color: 'var(--color-accent-fg)' }} />
              {mockStats.total_projects}
            </div>
            <div className="stat-label">Projects Analyzed</div>
          </div>
          <div className="text-center">
            <div className="stat-value flex items-center justify-center gap-2">
              <Users className="w-6 h-6" style={{ color: 'var(--color-success-fg)' }} />
              {mockStats.total_contributors.toLocaleString()}
            </div>
            <div className="stat-label">Contributors</div>
          </div>
          <div className="text-center">
            <div className="stat-value flex items-center justify-center gap-2">
              <GitFork className="w-6 h-6" style={{ color: 'var(--color-attention-fg)' }} />
              4
            </div>
            <div className="stat-label">Governance Categories</div>
          </div>
          <div className="text-center">
            <div className="stat-value flex items-center justify-center gap-2">
              <Star className="w-6 h-6" style={{ color: 'var(--color-done-fg)' }} />
              365
            </div>
            <div className="stat-label">Days of History</div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Governance Categories</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {(['federation', 'stadium', 'club', 'toy'] as const).map((category) => (
            <Link key={category} to={`/explore?category=${category}`}>
              <CategoryCard category={category} />
            </Link>
          ))}
        </div>
      </section>

      {/* Features */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">What You Can Do</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <Link
                key={feature.name}
                to={feature.href}
                className="card p-6 hover:border-opacity-60 transition-colors group"
              >
                <div className="flex items-start gap-4">
                  <div
                    className="w-10 h-10 rounded-lg flex items-center justify-center"
                    style={{ backgroundColor: 'var(--color-canvas-inset)' }}
                  >
                    <Icon className="w-5 h-5" style={{ color: 'var(--color-accent-fg)' }} />
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold group-hover:text-[var(--color-accent-fg)] transition-colors">
                      {feature.name}
                    </h3>
                    <p
                      className="text-sm mt-1"
                      style={{ color: 'var(--color-fg-muted)' }}
                    >
                      {feature.description}
                    </p>
                  </div>
                  <ArrowRight
                    className="w-5 h-5 opacity-0 group-hover:opacity-100 transition-opacity"
                    style={{ color: 'var(--color-fg-muted)' }}
                  />
                </div>
              </Link>
            )
          })}
        </div>
      </section>

      {/* How it works */}
      <section className="card p-6">
        <h2 className="text-xl font-semibold mb-4">How Classification Works</h2>
        <div className="prose prose-invert max-w-none text-sm" style={{ color: 'var(--color-fg-muted)' }}>
          <p>
            We analyze GitHub repositories using contributor entropy and governance patterns
            to classify them into one of four categories based on Elinor Ostrom's commons theory:
          </p>
          <ul className="mt-4 space-y-2">
            <li>
              <strong style={{ color: 'var(--color-federation)' }}>🏛️ Federation:</strong> High entropy,
              distributed contributions across multiple organizations (e.g., Kubernetes, Linux)
            </li>
            <li>
              <strong style={{ color: 'var(--color-stadium)' }}>🏟️ Stadium:</strong> High usage but
              concentrated maintenance, few core contributors (e.g., curl, zlib)
            </li>
            <li>
              <strong style={{ color: 'var(--color-club)' }}>🏠 Club:</strong> Moderate entropy,
              clear core team with community participation (e.g., Neovim, Flask)
            </li>
            <li>
              <strong style={{ color: 'var(--color-toy)' }}>🧸 Toy:</strong> Low entropy,
              single-maintainer personal projects (e.g., is-odd, colorama)
            </li>
          </ul>
        </div>
      </section>
    </div>
  )
}
