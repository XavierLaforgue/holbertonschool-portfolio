import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'

/**
 * Account page: shows who is logged in and lets them delete their account
 * themselves (RGPD right to erasure, article 17).
 */
export default function AccountPage() {
	const { user, isLoading, deleteAccount } = useAuth()
	const navigate = useNavigate()

	// render nothing while the auth context is still asking the back-end
	// who is logged in (otherwise "Log in" would flash for a moment)
	if (isLoading) return null

	// a logged-out visitor has no account to show
	if (!user) {
		return (
			<section className="mx-auto max-w-3xl px-4 py-12 text-sm">
				{/* `state.from` sends the visitor back here after logging in */}
				<Link to="/login" state={{ from: '/account' }} className="underline">
					Log in
				</Link>{' '}
				to see your account.
			</section>
		)
	}

	async function handleDeleteAccount() {
		// window.confirm() shows the browser's OK/Cancel dialog and
		// returns true only if the user clicks OK
		const confirmed = window.confirm(
			'Delete your account? Your recipes and photos will be deleted too. This cannot be undone.',
		)
		if (!confirmed) return
		try {
			// deletes the account, then sets the user to null (logged out)
			await deleteAccount()
			// go back to the home page
			navigate('/')
		} catch {
			window.alert('Your account could not be deleted. Please try again.')
		}
	}

	return (
		<section className="mx-auto max-w-3xl px-4 py-12">
			<h1 className="text-2xl font-bold md:text-3xl">My account</h1>
			<p className="mt-1 text-sm text-muted">Logged in as {user.email}</p>

			{/* a red border sets the irreversible action apart */}
			<div className="mt-10 rounded-md border border-primary p-4">
				<h2 className="text-lg font-semibold">Delete my account</h2>
				<p className="mt-1 text-sm text-muted">
					Deletes your account, your profile, your recipes and their
					photos, immediately and for good. Copies of your published
					recipes that other members saved stay in their account,
					without your name.
				</p>
				<button
					onClick={handleDeleteAccount}
					className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover hover:cursor-pointer transition-colors"
				>
					Delete my account
				</button>
			</div>
		</section>
	)
}
