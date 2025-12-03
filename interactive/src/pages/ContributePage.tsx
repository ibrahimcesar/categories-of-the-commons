import { useState } from 'react'
import { Github, AlertTriangle, CheckCircle, Loader2, Info, Lock } from 'lucide-react'
import CategoryBadge from '../components/CategoryBadge'
import type { GovernanceCategory } from '../types'

type Step = 'input' | 'consent' | 'processing' | 'result'

export default function ContributePage() {
  const [step, setStep] = useState<Step>('input')
  const [repoUrl, setRepoUrl] = useState('')
  const [token, setToken] = useState('')
  const [hypothesis, setHypothesis] = useState<GovernanceCategory | ''>('')
  const [consent, setConsent] = useState(false)
  const [error, setError] = useState('')

  // Mock result - will be replaced with API call
  const mockResult = {
    predicted: 'club' as GovernanceCategory,
    confidence: 0.78,
    metrics: {
      entropy: 2.45,
      normalized_entropy: 0.72,
      bus_factor: 5,
      contributors: 42,
    },
    similar: ['pallets/flask', 'fastapi/fastapi'],
  }

  const parseRepoUrl = (url: string): string | null => {
    // Handle various GitHub URL formats
    const patterns = [
      /github\.com\/([^\/]+\/[^\/]+)/,
      /^([^\/]+\/[^\/]+)$/,
    ]
    for (const pattern of patterns) {
      const match = url.match(pattern)
      if (match) {
        return match[1].replace(/\.git$/, '')
      }
    }
    return null
  }

  const handleSubmit = () => {
    const repo = parseRepoUrl(repoUrl)
    if (!repo) {
      setError('Invalid repository format. Use owner/repo or full GitHub URL.')
      return
    }
    if (!token.startsWith('ghp_') && !token.startsWith('github_pat_')) {
      setError('Invalid token format. Token should start with ghp_ or github_pat_')
      return
    }
    setError('')
    setStep('consent')
  }

  const handleConsent = () => {
    if (!consent) {
      setError('Please agree to the terms to continue.')
      return
    }
    setError('')
    setStep('processing')

    // Simulate API call
    setTimeout(() => {
      setStep('result')
    }, 3000)
  }

  const resetForm = () => {
    setStep('input')
    setRepoUrl('')
    setToken('')
    setHypothesis('')
    setConsent(false)
    setError('')
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Contribute to the Dataset</h1>
        <p className="mt-1" style={{ color: 'var(--color-fg-muted)' }}>
          Add your GitHub repository to the research dataset and see how it classifies
        </p>
      </div>

      {/* Step indicator */}
      <div className="flex items-center gap-2 text-sm" style={{ color: 'var(--color-fg-muted)' }}>
        {['Input', 'Consent', 'Processing', 'Result'].map((s, i) => {
          const stepNames: Step[] = ['input', 'consent', 'processing', 'result']
          const isActive = stepNames.indexOf(step) >= i
          return (
            <div key={s} className="flex items-center gap-2">
              {i > 0 && <div className="w-8 h-px" style={{ backgroundColor: isActive ? 'var(--color-accent-fg)' : 'var(--color-border-default)' }} />}
              <span className={isActive ? 'text-[var(--color-fg-default)]' : ''}>{s}</span>
            </div>
          )
        })}
      </div>

      {/* Input step */}
      {step === 'input' && (
        <div className="card p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium mb-2">
              GitHub Repository
            </label>
            <div className="relative">
              <Github
                className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5"
                style={{ color: 'var(--color-fg-subtle)' }}
              />
              <input
                type="text"
                placeholder="owner/repo or https://github.com/owner/repo"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                className="input pl-11"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              GitHub Personal Access Token
            </label>
            <div className="relative">
              <Lock
                className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5"
                style={{ color: 'var(--color-fg-subtle)' }}
              />
              <input
                type="password"
                placeholder="ghp_xxxx or github_pat_xxxx"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                className="input pl-11 font-mono"
              />
            </div>
            <p className="text-xs mt-1" style={{ color: 'var(--color-fg-subtle)' }}>
              Token is used only for this request and is never stored.
              <a
                href="https://github.com/settings/tokens/new?scopes=repo&description=Categories%20of%20the%20Commons"
                target="_blank"
                rel="noopener noreferrer"
                className="ml-1 underline hover:text-[var(--color-accent-fg)]"
              >
                Create a token →
              </a>
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Your Hypothesis (optional)
            </label>
            <p className="text-sm mb-2" style={{ color: 'var(--color-fg-muted)' }}>
              What governance category do you think this project belongs to?
            </p>
            <div className="flex flex-wrap gap-2">
              {(['', 'federation', 'stadium', 'club', 'toy'] as const).map((cat) => (
                <button
                  key={cat}
                  onClick={() => setHypothesis(cat)}
                  className={`px-3 py-1.5 text-sm rounded-md transition-colors ${
                    hypothesis === cat
                      ? 'bg-[var(--color-accent-emphasis)] text-white'
                      : 'bg-[var(--color-canvas-subtle)] hover:bg-[var(--color-border-muted)]'
                  }`}
                >
                  {cat === '' ? 'Not sure' : cat.charAt(0).toUpperCase() + cat.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg" style={{ backgroundColor: 'rgba(248, 81, 73, 0.1)' }}>
              <AlertTriangle className="w-5 h-5" style={{ color: 'var(--color-danger-fg)' }} />
              <span className="text-sm" style={{ color: 'var(--color-danger-fg)' }}>{error}</span>
            </div>
          )}

          <button onClick={handleSubmit} className="btn btn-primary w-full">
            Continue
          </button>
        </div>
      )}

      {/* Consent step */}
      {step === 'consent' && (
        <div className="card p-6 space-y-6">
          <div className="flex items-start gap-3 p-4 rounded-lg" style={{ backgroundColor: 'rgba(88, 166, 255, 0.1)' }}>
            <Info className="w-5 h-5 shrink-0 mt-0.5" style={{ color: 'var(--color-accent-fg)' }} />
            <div className="text-sm space-y-2" style={{ color: 'var(--color-fg-muted)' }}>
              <p><strong>What we'll collect:</strong></p>
              <ul className="list-disc list-inside space-y-1">
                <li>Repository metadata (stars, forks, language)</li>
                <li>Contributor statistics (usernames, contribution counts)</li>
                <li>Recent commit history (365 days)</li>
                <li>Governance files presence</li>
              </ul>
              <p className="mt-3"><strong>What we won't collect:</strong></p>
              <ul className="list-disc list-inside space-y-1">
                <li>Source code contents</li>
                <li>Private repository data</li>
                <li>Personal identifying information</li>
              </ul>
            </div>
          </div>

          <div className="space-y-3">
            <label className="flex items-start gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
                className="mt-1"
              />
              <span className="text-sm">
                I agree to contribute this repository's public metadata to the Categories of the Commons
                research dataset. I understand this data will be used for academic research and may be
                published in aggregated form.
              </span>
            </label>
          </div>

          {error && (
            <div className="flex items-center gap-2 p-3 rounded-lg" style={{ backgroundColor: 'rgba(248, 81, 73, 0.1)' }}>
              <AlertTriangle className="w-5 h-5" style={{ color: 'var(--color-danger-fg)' }} />
              <span className="text-sm" style={{ color: 'var(--color-danger-fg)' }}>{error}</span>
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={() => setStep('input')} className="btn btn-secondary flex-1">
              Back
            </button>
            <button onClick={handleConsent} className="btn btn-primary flex-1">
              Analyze Repository
            </button>
          </div>
        </div>
      )}

      {/* Processing step */}
      {step === 'processing' && (
        <div className="card p-12 text-center">
          <Loader2 className="w-12 h-12 mx-auto animate-spin" style={{ color: 'var(--color-accent-fg)' }} />
          <h3 className="text-lg font-semibold mt-4">Analyzing Repository</h3>
          <p className="mt-2" style={{ color: 'var(--color-fg-muted)' }}>
            Collecting contributor data and computing metrics...
          </p>
          <p className="text-sm mt-4" style={{ color: 'var(--color-fg-subtle)' }}>
            This usually takes 30-60 seconds depending on repository size.
          </p>
        </div>
      )}

      {/* Result step */}
      {step === 'result' && (
        <div className="space-y-6">
          <div className="card p-6 text-center">
            <CheckCircle className="w-12 h-12 mx-auto" style={{ color: 'var(--color-success-fg)' }} />
            <h3 className="text-lg font-semibold mt-4">Analysis Complete!</h3>

            <div className="mt-6">
              <p className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>
                Predicted Category
              </p>
              <div className="mt-2">
                <CategoryBadge category={mockResult.predicted} size="lg" />
              </div>
              <p className="text-sm mt-2" style={{ color: 'var(--color-fg-muted)' }}>
                Confidence: {(mockResult.confidence * 100).toFixed(0)}%
              </p>
            </div>

            {hypothesis && hypothesis !== mockResult.predicted && (
              <div className="mt-4 p-3 rounded-lg" style={{ backgroundColor: 'rgba(210, 153, 34, 0.1)' }}>
                <p className="text-sm" style={{ color: 'var(--color-attention-fg)' }}>
                  Your hypothesis was <strong>{hypothesis}</strong> — interesting difference!
                </p>
              </div>
            )}

            {hypothesis && hypothesis === mockResult.predicted && (
              <div className="mt-4 p-3 rounded-lg" style={{ backgroundColor: 'rgba(63, 185, 80, 0.1)' }}>
                <p className="text-sm" style={{ color: 'var(--color-success-fg)' }}>
                  Your hypothesis was correct! 🎉
                </p>
              </div>
            )}
          </div>

          {/* Metrics */}
          <div className="card p-6">
            <h4 className="font-semibold mb-4">Computed Metrics</h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-mono font-semibold">
                  {mockResult.metrics.entropy.toFixed(2)}
                </div>
                <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Entropy</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-mono font-semibold">
                  {mockResult.metrics.normalized_entropy.toFixed(2)}
                </div>
                <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Normalized</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-mono font-semibold">
                  {mockResult.metrics.bus_factor}
                </div>
                <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Bus Factor</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-mono font-semibold">
                  {mockResult.metrics.contributors}
                </div>
                <div className="text-sm" style={{ color: 'var(--color-fg-muted)' }}>Contributors</div>
              </div>
            </div>
          </div>

          {/* Similar projects */}
          <div className="card p-6">
            <h4 className="font-semibold mb-4">Similar Projects in Dataset</h4>
            <div className="flex flex-wrap gap-2">
              {mockResult.similar.map((repo) => (
                <a
                  key={repo}
                  href={`https://github.com/${repo}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-3 py-1.5 text-sm rounded-md bg-[var(--color-canvas-subtle)] hover:bg-[var(--color-border-muted)] transition-colors"
                >
                  {repo}
                </a>
              ))}
            </div>
          </div>

          <button onClick={resetForm} className="btn btn-secondary w-full">
            Analyze Another Repository
          </button>
        </div>
      )}

      {/* Rate limit info */}
      <div className="text-center text-sm" style={{ color: 'var(--color-fg-subtle)' }}>
        <p>Each repository can be analyzed once per day to respect API limits.</p>
      </div>
    </div>
  )
}
