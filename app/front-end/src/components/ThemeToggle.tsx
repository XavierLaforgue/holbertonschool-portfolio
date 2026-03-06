import { useEffect, useState } from 'react'

const THEME_KEY = 'theme'

function getInitialTheme(): 'light' | 'dark' {
	if (typeof window === 'undefined') return 'light'
	const stored = localStorage.getItem(THEME_KEY)
	if (stored === 'dark' || stored === 'light') return stored
	return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export default function ThemeToggle() {
	const [theme, setTheme] = useState<'light' | 'dark'>(getInitialTheme)

	useEffect(() => {
		const root = document.documentElement
		if (theme === 'dark') {
			root.classList.add('dark')
		} else {
			root.classList.remove('dark')
		}
		localStorage.setItem(THEME_KEY, theme)
	}, [theme])

	return (
		<button
			onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}
			className="rounded-md p-2 text-muted hover:bg-surface-hover transition-colors"
			aria-label={`Change to ${theme === 'dark' ? 'light' : 'dark'} mode`}
			title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
		>
			{theme === 'dark' ? (
				// Sun icon
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5">
					<path d="M10 2a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 10 2ZM10 15a.75.75 0 0 1 .75.75v1.5a.75.75 0 0 1-1.5 0v-1.5A.75.75 0 0 1 10 15ZM10 7a3 3 0 1 0 0 6 3 3 0 0 0 0-6ZM15.657 5.404a.75.75 0 1 0-1.06-1.06l-1.061 1.06a.75.75 0 0 0 1.06 1.06l1.06-1.06ZM6.464 14.596a.75.75 0 1 0-1.06-1.06l-1.06 1.06a.75.75 0 0 0 1.06 1.06l1.06-1.06ZM18 10a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5A.75.75 0 0 1 18 10ZM5 10a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1 0-1.5h1.5A.75.75 0 0 1 5 10ZM14.596 15.657a.75.75 0 0 0 1.06-1.06l-1.06-1.061a.75.75 0 1 0-1.06 1.06l1.06 1.06ZM5.404 6.464a.75.75 0 0 0 1.06-1.06l-1.06-1.06a.75.75 0 1 0-1.06 1.06l1.06 1.06Z" />
				</svg>
			) : (
				// Moon icon
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5">
					<path fillRule="evenodd" d="M7.455 2.004a.75.75 0 0 1 .26.77 7 7 0 0 0 9.958 7.967.75.75 0 0 1 1.067.853A8.5 8.5 0 1 1 6.647 1.921a.75.75 0 0 1 .808.083Z" clipRule="evenodd" />
				</svg>
			)}
		</button>
	)
}
