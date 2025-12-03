import clsx from 'clsx'
import type { GovernanceCategory } from '../types'

interface CategoryBadgeProps {
  category: GovernanceCategory
  size?: 'sm' | 'md' | 'lg'
}

const categoryInfo = {
  federation: {
    label: 'Federation',
    description: 'Distributed governance, multiple organizations',
    emoji: '🏛️',
  },
  stadium: {
    label: 'Stadium',
    description: 'High usage, few maintainers',
    emoji: '🏟️',
  },
  club: {
    label: 'Club',
    description: 'Core team with community',
    emoji: '🏠',
  },
  toy: {
    label: 'Toy',
    description: 'Single maintainer, personal project',
    emoji: '🧸',
  },
}

export default function CategoryBadge({ category, size = 'md' }: CategoryBadgeProps) {
  const info = categoryInfo[category]

  return (
    <span
      className={clsx(
        'label',
        `label-${category}`,
        size === 'sm' && 'text-xs px-2 py-0.5',
        size === 'md' && 'text-sm px-2.5 py-1',
        size === 'lg' && 'text-base px-3 py-1.5'
      )}
      title={info.description}
    >
      <span className="mr-1">{info.emoji}</span>
      {info.label}
    </span>
  )
}

export function CategoryCard({ category }: { category: GovernanceCategory }) {
  const info = categoryInfo[category]

  return (
    <div className={clsx('card p-4 hover:border-opacity-60 transition-colors cursor-pointer')}>
      <div className="flex items-start gap-3">
        <span className="text-2xl">{info.emoji}</span>
        <div>
          <h3 className="font-semibold">{info.label}</h3>
          <p className="text-sm mt-1" style={{ color: 'var(--color-fg-muted)' }}>
            {info.description}
          </p>
        </div>
      </div>
    </div>
  )
}
