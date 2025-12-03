import { Link, useLocation } from 'react-router-dom'
import {
  Home,
  Search,
  Calculator,
  GitCompare,
  Plus,
  Github,
  BookOpen,
  Star
} from 'lucide-react'
import clsx from 'clsx'

interface LayoutProps {
  children: React.ReactNode
}

const navigation = [
  { name: 'Home', href: '/', icon: Home },
  { name: 'Explore', href: '/explore', icon: Search },
  { name: 'Equations', href: '/equations', icon: Calculator },
  { name: 'Compare', href: '/compare', icon: GitCompare },
  { name: 'Contribute', href: '/contribute', icon: Plus },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  return (
    <div className="min-h-screen flex flex-col">
      {/* GitHub-style header */}
      <header
        className="sticky top-0 z-50 px-4 py-3"
        style={{
          backgroundColor: 'var(--color-canvas-subtle)',
          borderBottom: '1px solid var(--color-border-default)'
        }}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div
              className="w-8 h-8 rounded-full flex items-center justify-center"
              style={{ backgroundColor: 'var(--color-accent-emphasis)' }}
            >
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold text-lg hidden sm:inline">
              Categories of the Commons
            </span>
          </Link>

          {/* Navigation */}
          <nav className="flex items-center gap-1">
            {navigation.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={clsx(
                    'nav-item flex items-center gap-2',
                    isActive && 'active'
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span className="hidden md:inline">{item.name}</span>
                </Link>
              )
            })}
          </nav>

          {/* GitHub link */}
          <a
            href="https://github.com/ibrahimcesar/categories-of-the-commons"
            target="_blank"
            rel="noopener noreferrer"
            className="nav-item flex items-center gap-2"
          >
            <Github className="w-5 h-5" />
            <Star className="w-4 h-4" />
          </a>
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 py-6">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer
        className="px-4 py-6 text-center text-sm"
        style={{
          backgroundColor: 'var(--color-canvas-subtle)',
          borderTop: '1px solid var(--color-border-default)',
          color: 'var(--color-fg-muted)'
        }}
      >
        <p>
          Part of the <strong>Categories of the Commons</strong> research project.
        </p>
        <p className="mt-1">
          Studying open source governance through the lens of commons theory.
        </p>
      </footer>
    </div>
  )
}
