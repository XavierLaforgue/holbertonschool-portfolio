import { useEffect, useState } from 'react'

const THEME_KEY = 'theme'

function getInitialTheme(): 'light' | 'dark' {
	// in case of SSR (later on, using react router v7 framework,
	// perhaps) `window` doesn't exist
	if (typeof window === 'undefined') return 'dark'
	// check localStorage, where the value will be stored by the component 
	const stored = localStorage.getItem(THEME_KEY)
	if (stored === 'dark' || stored === 'light') return stored
	// default to system
	return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export default function ThemeToggle() {
	const [theme, setTheme] = useState<'light' | 'dark'>(getInitialTheme)

	// on change of theme, add class dark to all classes if theme=dark, remove
	// it otherwise
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
			onClick={() => setTheme((_theme) => (
				_theme === 'dark' ? 'light' : 'dark')
			)}
			className="rounded-md p-2 text-muted hover:bg-surface-hover transition-colors cursor-pointer"
			aria-label={`Change to ${theme === 'dark' ? 'light' : 'dark'} mode`}
			title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
		>
			{theme === 'dark' ? (
				// Sun icon
				<svg 
					xmlns="http://www.w3.org/2000/svg" 
					width="24" height="24" viewBox="0 0 24 24" 
					fill="none" stroke="currentColor" stroke-width="2"
					stroke-linecap="round" stroke-linejoin="round"
					className="lucide lucide-sun-icon lucide-sun h-5 w-5"
				>
					<circle cx="12" cy="12" r="4"/>
					<path d="M12 2v2"/>
					<path d="M12 20v2"/>
					<path d="m4.93 4.93 1.41 1.41"/>
					<path d="m17.66 17.66 1.41 1.41"/>
					<path d="M2 12h2"/>
					<path d="M20 12h2"/>
					<path d="m6.34 17.66-1.41 1.41"/>
					<path d="m19.07 4.93-1.41 1.41"/>
				</svg>
			) : (
				// Moon icon
				<svg 
					xmlns="http://www.w3.org/2000/svg"
					width="24" height="24" viewBox="0 0 24 24"
					fill="currentColor" stroke="none" stroke-width="2"
					stroke-linecap="round" stroke-linejoin="round"
					className="lucide lucide-moon-icon lucide-moon h-5 w-5"
				>
					<path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"/>
				</svg>
			)}
		</button>
	)
}
