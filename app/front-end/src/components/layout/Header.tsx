import SiteLogo from '@/components/branding/SiteLogo.tsx'
import NavBar from '@/components/navigation/NavBar.tsx'
import UserMenu from '@/components/auth/UserMenu.tsx'
import ThemeToggle from '@/components/navigation/ThemeToggle.tsx'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

export default function Header() {
	const { user, isLoading } = useAuth()
	const location = useLocation()

	return (
		<header className="flex items-center justify-between border-b border-border px-6 py-3">
			<SiteLogo />

			<div className="flex items-center gap-6">
				<NavBar />
				<ThemeToggle />
				{isLoading ? null : user ? (
					<UserMenu />
				) : (
					<Link
						to="/login"
						state={{ from: location.pathname }}
						className="shrink-0 whitespace-nowrap rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover transition-colors"
					>
						Log in
					</Link>
				)}
			</div>
		</header>
	)
}
