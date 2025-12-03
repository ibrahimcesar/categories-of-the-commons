import { useState } from 'react'
import { InlineMath, BlockMath } from 'react-katex'
import { Lightbulb, Play } from 'lucide-react'

interface InteractiveExample {
  contributions: number[]
  name: string
}

const examples: InteractiveExample[] = [
  { name: 'Equal (4 contributors)', contributions: [25, 25, 25, 25] },
  { name: 'Dominated (1 main + 3 small)', contributions: [85, 5, 5, 5] },
  { name: 'Typical Club', contributions: [40, 25, 20, 10, 5] },
  { name: 'Federation-like', contributions: [15, 14, 13, 12, 11, 10, 9, 8, 8] },
  { name: 'Toy (single maintainer)', contributions: [95, 3, 2] },
]

function calculateEntropy(contributions: number[]): number {
  const total = contributions.reduce((a, b) => a + b, 0)
  const probabilities = contributions.map((c) => c / total)
  return -probabilities.reduce((sum, p) => {
    if (p === 0) return sum
    return sum + p * Math.log2(p)
  }, 0)
}

function calculateNormalizedEntropy(contributions: number[]): number {
  const entropy = calculateEntropy(contributions)
  const maxEntropy = Math.log2(contributions.length)
  return maxEntropy > 0 ? entropy / maxEntropy : 0
}

function calculateGini(contributions: number[]): number {
  const sorted = [...contributions].sort((a, b) => a - b)
  const n = sorted.length
  const total = sorted.reduce((a, b) => a + b, 0)

  let sumOfDiffs = 0
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      sumOfDiffs += Math.abs(sorted[i] - sorted[j])
    }
  }

  return sumOfDiffs / (2 * n * n * (total / n))
}

export default function EquationsPage() {
  const [selectedExample, setSelectedExample] = useState(0)
  const [customContributions, setCustomContributions] = useState('40, 25, 20, 10, 5')

  const currentContributions = examples[selectedExample].contributions
  const entropy = calculateEntropy(currentContributions)
  const normalizedEntropy = calculateNormalizedEntropy(currentContributions)
  const gini = calculateGini(currentContributions)

  // Parse custom contributions
  let customParsed: number[] = []
  let customEntropy = 0
  let customNormalized = 0
  let customGini = 0
  try {
    customParsed = customContributions
      .split(',')
      .map((s) => parseFloat(s.trim()))
      .filter((n) => !isNaN(n) && n > 0)
    if (customParsed.length > 0) {
      customEntropy = calculateEntropy(customParsed)
      customNormalized = calculateNormalizedEntropy(customParsed)
      customGini = calculateGini(customParsed)
    }
  } catch {
    // Invalid input
  }

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold">Interactive Equations</h1>
        <p className="mt-1" style={{ color: 'var(--color-fg-muted)' }}>
          Understand the math behind governance metrics with live calculations
        </p>
      </div>

      {/* Shannon Entropy */}
      <section className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <span className="text-2xl">📊</span>
          Shannon Entropy
        </h2>

        <p style={{ color: 'var(--color-fg-muted)' }}>
          Measures the "disorder" or "diversity" of contributions. Higher entropy means more
          distributed contributions; lower entropy means more concentrated.
        </p>

        <div
          className="p-4 rounded-lg overflow-x-auto"
          style={{ backgroundColor: 'var(--color-canvas-inset)' }}
        >
          <BlockMath math="H(X) = -\sum_{i=1}^{n} p_i \log_2(p_i)" />
        </div>

        <div className="text-sm space-y-1" style={{ color: 'var(--color-fg-muted)' }}>
          <p>
            Where <InlineMath math="p_i" /> is the probability (proportion) of contributor{' '}
            <InlineMath math="i" />'s contributions.
          </p>
          <p>
            For a project with contributions [40, 30, 20, 10], the probabilities are [0.4, 0.3, 0.2, 0.1].
          </p>
        </div>

        {/* Interactive example */}
        <div className="border rounded-lg p-4" style={{ borderColor: 'var(--color-border-default)' }}>
          <h3 className="font-medium mb-3 flex items-center gap-2">
            <Play className="w-4 h-4" style={{ color: 'var(--color-success-fg)' }} />
            Interactive Example
          </h3>

          <div className="flex flex-wrap gap-2 mb-4">
            {examples.map((ex, i) => (
              <button
                key={i}
                onClick={() => setSelectedExample(i)}
                className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                  selectedExample === i
                    ? 'bg-[var(--color-accent-emphasis)] text-white'
                    : 'bg-[var(--color-canvas-subtle)] hover:bg-[var(--color-border-muted)]'
                }`}
              >
                {ex.name}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm mb-2" style={{ color: 'var(--color-fg-muted)' }}>
                Contributions: [{currentContributions.join(', ')}]
              </p>

              {/* Bar visualization */}
              <div className="flex items-end h-24 gap-1">
                {currentContributions.map((c, i) => {
                  const height = (c / Math.max(...currentContributions)) * 100
                  return (
                    <div
                      key={i}
                      className="flex-1 rounded-t transition-all"
                      style={{
                        height: `${height}%`,
                        backgroundColor: 'var(--color-accent-fg)',
                        opacity: 0.5 + (c / currentContributions.reduce((a, b) => a + b, 0)) * 0.5,
                      }}
                      title={`Contributor ${i + 1}: ${c}`}
                    />
                  )
                })}
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between">
                <span style={{ color: 'var(--color-fg-muted)' }}>Entropy (H):</span>
                <span className="font-mono font-semibold">{entropy.toFixed(4)} bits</span>
              </div>
              <div className="flex justify-between">
                <span style={{ color: 'var(--color-fg-muted)' }}>Normalized (H/H_max):</span>
                <span className="font-mono font-semibold">{normalizedEntropy.toFixed(4)}</span>
              </div>
              <div className="flex justify-between">
                <span style={{ color: 'var(--color-fg-muted)' }}>Max possible (log₂ n):</span>
                <span className="font-mono">{Math.log2(currentContributions.length).toFixed(4)} bits</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Gini Coefficient */}
      <section className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <span className="text-2xl">📈</span>
          Gini Coefficient
        </h2>

        <p style={{ color: 'var(--color-fg-muted)' }}>
          Measures inequality in contributions. 0 = perfect equality (everyone contributes equally),
          1 = perfect inequality (one person does everything).
        </p>

        <div
          className="p-4 rounded-lg overflow-x-auto"
          style={{ backgroundColor: 'var(--color-canvas-inset)' }}
        >
          <BlockMath math="G = \frac{\sum_{i=1}^{n}\sum_{j=1}^{n}|x_i - x_j|}{2n^2\bar{x}}" />
        </div>

        <div className="flex justify-between items-center p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-subtle)' }}>
          <span>Gini for current example:</span>
          <span className="font-mono text-xl font-semibold">{gini.toFixed(4)}</span>
        </div>
      </section>

      {/* Bus Factor */}
      <section className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <span className="text-2xl">🚌</span>
          Bus Factor
        </h2>

        <p style={{ color: 'var(--color-fg-muted)' }}>
          The minimum number of contributors who would need to leave for the project to
          lose more than 50% of its knowledge/contributions.
        </p>

        <div
          className="p-4 rounded-lg"
          style={{ backgroundColor: 'var(--color-canvas-inset)' }}
        >
          <BlockMath math="\text{Bus Factor} = \min\{k : \sum_{i=1}^{k} c_i \geq 0.5 \times \sum_{i=1}^{n} c_i\}" />
        </div>

        <div
          className="flex items-start gap-3 p-4 rounded-lg"
          style={{ backgroundColor: 'rgba(210, 153, 34, 0.1)' }}
        >
          <Lightbulb className="w-5 h-5 shrink-0" style={{ color: 'var(--color-attention-fg)' }} />
          <p className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>
            A bus factor of 1 is a warning sign — the project depends entirely on one person.
            Higher is better for sustainability.
          </p>
        </div>
      </section>

      {/* Try your own */}
      <section className="card p-6 space-y-4">
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <span className="text-2xl">🧪</span>
          Try Your Own
        </h2>

        <p style={{ color: 'var(--color-fg-muted)' }}>
          Enter contribution values separated by commas to see the metrics:
        </p>

        <input
          type="text"
          value={customContributions}
          onChange={(e) => setCustomContributions(e.target.value)}
          className="input font-mono"
          placeholder="40, 25, 20, 10, 5"
        />

        {customParsed.length > 0 && (
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-subtle)' }}>
              <div className="text-2xl font-mono font-semibold">{customEntropy.toFixed(3)}</div>
              <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Entropy</div>
            </div>
            <div className="text-center p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-subtle)' }}>
              <div className="text-2xl font-mono font-semibold">{customNormalized.toFixed(3)}</div>
              <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Normalized</div>
            </div>
            <div className="text-center p-4 rounded-lg" style={{ backgroundColor: 'var(--color-canvas-subtle)' }}>
              <div className="text-2xl font-mono font-semibold">{customGini.toFixed(3)}</div>
              <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Gini</div>
            </div>
          </div>
        )}
      </section>
    </div>
  )
}
