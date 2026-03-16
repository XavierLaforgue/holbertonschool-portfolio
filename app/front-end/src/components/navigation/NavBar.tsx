import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { apiCreateRecipe } from '../../lib/api-recipes'

const navLinks = [
	{ to: '/#featured-recipes', label: 'Explore' },
	// { to: '/experience', label: 'Experience' },
]

const linkClasses =
	'text-sm font-medium text-subtle hover:text-foreground transition-colors'

export default function NavBar() {
	const [open, setOpen] = useState(false)
	const [creating, setCreating] = useState(false)
	const { user } = useAuth()
	const navigate = useNavigate()
	const location = useLocation()

	async function handleCreate() {
		if (!user) {
			const from = `${location.pathname}${location.search}${location.hash}`
			navigate('/login', {
				state: { from, error: 'Please log in to create recipes.' },
			})
			return
		}
		setCreating(true)
		try {
			const recipe = await apiCreateRecipe()
			navigate(`/recipes/${recipe.id}/edit`)
		} finally {
			setCreating(false)
		}
	}

	const CreateButton = ({ mobile }: { mobile?: boolean }) => (
		<button
			onClick={() => { setOpen(false); handleCreate() }}
			disabled={creating}
			className={
				mobile
					? 'block w-full text-left px-4 py-2 text-sm text-subtle hover:bg-surface-hover transition-colors disabled:opacity-50 cursor-pointer z-10'
					: `${linkClasses} cursor-pointer disabled:opacity-50`
			}
		>
			{creating ? 'Creating…' : 'Create'}
		</button>
	)

	return (
		<>
			{/* Desktop nav */}
			<nav className="hidden md:flex items-center gap-4">
				{navLinks.map((link) => (
					<Link key={link.to} to={link.to} className={linkClasses}>
						{link.label}
					</Link>
				))}
				<CreateButton />
			</nav>

			{/* Mobile hamburger */}
			<div className="relative md:hidden">
				<button
					onClick={() => setOpen((prev) => !prev)}
					className="rounded-md p-2 text-muted hover:bg-surface-hover transition-colors"
					aria-label="Toggle navigation menu"
				>
					{open ? (
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5">
							<path d="M6.28 5.22a.75.75 0 0 0-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 1 0 1.06 1.06L10 11.06l3.72 3.72a.75.75 0 1 0 1.06-1.06L11.06 10l3.72-3.72a.75.75 0 0 0-1.06-1.06L10 8.94 6.28 5.22Z" />
						</svg>
					) : (
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="h-5 w-5">
							<path fillRule="evenodd" d="M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 4.75ZM2 10a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 10Zm0 5.25a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1-.75-.75Z" clipRule="evenodd" />
						</svg>
					)}
				</button>

				{open && (
					<nav className="absolute right-0 mt-2 w-44 rounded-md border border-input bg-surface py-1 shadow-lg z-1000">
						{navLinks.map((link) => (
							<Link
								key={link.to}
								to={link.to}
								onClick={() => setOpen(false)}
								className="block px-4 py-2 text-sm text-subtle hover:bg-surface-hover transition-colors"
							>
								{link.label}
							</Link>
						))}
						<CreateButton mobile />
					</nav>
				)}
			</div>
		</>
	)
}
