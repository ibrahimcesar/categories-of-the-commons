import { useState } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  Cell,
} from 'recharts'
import CategoryBadge from '../components/CategoryBadge'
import type { GovernanceCategory } from '../types'

// Mock data - will be replaced with API call
const categoryStats = [
  { category: 'federation', avg_entropy: 3.8, avg_bus_factor: 28, avg_contributors: 1850, count: 19 },
  { category: 'stadium', avg_entropy: 1.5, avg_bus_factor: 3, avg_contributors: 420, count: 37 },
  { category: 'club', avg_entropy: 2.6, avg_bus_factor: 9, avg_contributors: 680, count: 19 },
  { category: 'toy', avg_entropy: 1.0, avg_bus_factor: 1, avg_contributors: 85, count: 16 },
]

const scatterData = [
  { repo: 'kubernetes/kubernetes', category: 'federation', entropy: 4.2, bus_factor: 45, contributors: 3500 },
  { repo: 'nodejs/node', category: 'federation', entropy: 3.9, bus_factor: 38, contributors: 3200 },
  { repo: 'grafana/grafana', category: 'federation', entropy: 3.5, bus_factor: 28, contributors: 2100 },
  { repo: 'curl/curl', category: 'stadium', entropy: 1.8, bus_factor: 3, contributors: 890 },
  { repo: 'axios/axios', category: 'stadium', entropy: 1.5, bus_factor: 4, contributors: 420 },
  { repo: 'lodash/lodash', category: 'stadium', entropy: 1.3, bus_factor: 2, contributors: 320 },
  { repo: 'zlib', category: 'stadium', entropy: 0.9, bus_factor: 1, contributors: 45 },
  { repo: 'neovim/neovim', category: 'club', entropy: 2.8, bus_factor: 12, contributors: 1200 },
  { repo: 'pallets/flask', category: 'club', entropy: 2.5, bus_factor: 8, contributors: 680 },
  { repo: 'fastapi/fastapi', category: 'club', entropy: 2.3, bus_factor: 6, contributors: 520 },
  { repo: 'BurntSushi/ripgrep', category: 'toy', entropy: 1.2, bus_factor: 1, contributors: 380 },
  { repo: 'sindresorhus/is-odd', category: 'toy', entropy: 0.8, bus_factor: 1, contributors: 12 },
  { repo: 'dtolnay/anyhow', category: 'toy', entropy: 0.9, bus_factor: 1, contributors: 65 },
]

const categoryColors: Record<GovernanceCategory, string> = {
  federation: '#58a6ff',
  stadium: '#d29922',
  club: '#3fb950',
  toy: '#a371f7',
}

export default function ComparePage() {
  const [metric, setMetric] = useState<'entropy' | 'bus_factor' | 'contributors'>('entropy')

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Compare Categories</h1>
        <p className="mt-1" style={{ color: 'var(--color-fg-muted)' }}>
          Visualize and compare metrics across governance categories
        </p>
      </div>

      {/* Category averages */}
      <section className="card p-6">
        <h2 className="text-lg font-semibold mb-4">Category Averages</h2>

        <div className="flex gap-2 mb-6">
          {(['entropy', 'bus_factor', 'contributors'] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMetric(m)}
              className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                metric === m
                  ? 'bg-[var(--color-accent-emphasis)] text-white'
                  : 'bg-[var(--color-canvas-subtle)] hover:bg-[var(--color-border-muted)]'
              }`}
            >
              {m === 'entropy' ? 'Entropy' : m === 'bus_factor' ? 'Bus Factor' : 'Contributors'}
            </button>
          ))}
        </div>

        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={categoryStats}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-muted)" />
              <XAxis
                dataKey="category"
                tick={{ fill: 'var(--color-fg-muted)' }}
                tickFormatter={(v) => v.charAt(0).toUpperCase() + v.slice(1)}
              />
              <YAxis tick={{ fill: 'var(--color-fg-muted)' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'var(--color-canvas-subtle)',
                  border: '1px solid var(--color-border-default)',
                  borderRadius: '6px',
                }}
                labelStyle={{ color: 'var(--color-fg-default)' }}
              />
              <Bar
                dataKey={metric === 'entropy' ? 'avg_entropy' : metric === 'bus_factor' ? 'avg_bus_factor' : 'avg_contributors'}
                name={metric === 'entropy' ? 'Avg Entropy' : metric === 'bus_factor' ? 'Avg Bus Factor' : 'Avg Contributors'}
              >
                {categoryStats.map((entry) => (
                  <Cell key={entry.category} fill={categoryColors[entry.category as GovernanceCategory]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Legend */}
        <div className="flex justify-center gap-6 mt-4">
          {categoryStats.map((cat) => (
            <div key={cat.category} className="flex items-center gap-2">
              <div
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: categoryColors[cat.category as GovernanceCategory] }}
              />
              <span className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>
                {cat.category.charAt(0).toUpperCase() + cat.category.slice(1)} ({cat.count})
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Scatter plot */}
      <section className="card p-6">
        <h2 className="text-lg font-semibold mb-4">Entropy vs Bus Factor</h2>
        <p className="text-sm mb-4" style={{ color: 'var(--color-fg-muted)' }}>
          Each dot represents a project. Notice how categories cluster in different regions.
        </p>

        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border-muted)" />
              <XAxis
                type="number"
                dataKey="entropy"
                name="Entropy"
                tick={{ fill: 'var(--color-fg-muted)' }}
                label={{ value: 'Entropy', position: 'bottom', fill: 'var(--color-fg-muted)' }}
              />
              <YAxis
                type="number"
                dataKey="bus_factor"
                name="Bus Factor"
                tick={{ fill: 'var(--color-fg-muted)' }}
                label={{ value: 'Bus Factor', angle: -90, position: 'left', fill: 'var(--color-fg-muted)' }}
              />
              <Tooltip
                cursor={{ strokeDasharray: '3 3' }}
                contentStyle={{
                  backgroundColor: 'var(--color-canvas-subtle)',
                  border: '1px solid var(--color-border-default)',
                  borderRadius: '6px',
                }}
                formatter={(value, name) => [value, name]}
                labelFormatter={(_, payload) => payload[0]?.payload?.repo || ''}
              />
              <Legend />
              {(['federation', 'stadium', 'club', 'toy'] as const).map((category) => (
                <Scatter
                  key={category}
                  name={category.charAt(0).toUpperCase() + category.slice(1)}
                  data={scatterData.filter((d) => d.category === category)}
                  fill={categoryColors[category]}
                />
              ))}
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Category summary table */}
      <section className="card overflow-hidden">
        <h2 className="text-lg font-semibold p-6 pb-0">Category Summary</h2>
        <div className="overflow-x-auto">
          <table className="table mt-4">
            <thead>
              <tr>
                <th>Category</th>
                <th className="text-right">Projects</th>
                <th className="text-right">Avg Entropy</th>
                <th className="text-right">Avg Bus Factor</th>
                <th className="text-right">Avg Contributors</th>
              </tr>
            </thead>
            <tbody>
              {categoryStats.map((cat) => (
                <tr key={cat.category}>
                  <td>
                    <CategoryBadge category={cat.category as GovernanceCategory} />
                  </td>
                  <td className="text-right font-mono">{cat.count}</td>
                  <td className="text-right font-mono">{cat.avg_entropy.toFixed(2)}</td>
                  <td className="text-right font-mono">{cat.avg_bus_factor}</td>
                  <td className="text-right font-mono">{cat.avg_contributors.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Insights */}
      <section className="card p-6">
        <h2 className="text-lg font-semibold mb-4">Key Insights</h2>
        <div className="grid md:grid-cols-2 gap-4 text-sm" style={{ color: 'var(--color-fg-muted)' }}>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-inset)' }}>
            <h3 className="font-medium text-[var(--color-federation)] mb-2">🏛️ Federation</h3>
            <p>
              Highest entropy and bus factor. Contributions distributed across many organizations.
              Most resilient to contributor loss.
            </p>
          </div>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-inset)' }}>
            <h3 className="font-medium text-[var(--color-stadium)] mb-2">🏟️ Stadium</h3>
            <p>
              Low entropy, low bus factor despite many users. High risk of maintainer burnout.
              Critical infrastructure often falls here.
            </p>
          </div>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-inset)' }}>
            <h3 className="font-medium text-[var(--color-club)] mb-2">🏠 Club</h3>
            <p>
              Moderate entropy with clear core team. Community contributions welcome but
              leadership is defined. Good balance.
            </p>
          </div>
          <div className="p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-inset)' }}>
            <h3 className="font-medium text-[var(--color-toy)] mb-2">🧸 Toy</h3>
            <p>
              Lowest entropy, single maintainer. Often personal utilities that became popular.
              Sustainability depends entirely on one person.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
