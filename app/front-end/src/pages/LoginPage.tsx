import { useState, type SubmitEvent } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useNavigate, useLocation, Link } from 'react-router-dom'
import { ApiError } from '../lib/api'

export default function LoginPage() {
	const { login } = useAuth()
	const navigate = useNavigate()
	const location = useLocation()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const authState = location.state as { from?: string; error?: string } | null
	const [error, setError] = useState<string | null>(authState?.error ?? null)
	const [isSubmitting, setIsSubmitting] = useState(false)
	// We arrive here from a page that set their location in the state
	// as the value with key `from`.
	// We recover that state at the authentication-related pages (login/signup)
	// extract `from` value safely from the state
	const requestedFrom = authState?.from
	// store it into `from` variable safely and if it doesn't involve
	// `/login` or `/signup` paths, otherwise default to the home
	// page
	const from = requestedFrom && !['/login', '/signup'].includes(requestedFrom) ? requestedFrom : '/'

	const handleSubmit = async (e: SubmitEvent) => {
		e.preventDefault()
		setError(null)
		setIsSubmitting(true)
		try {
			await login(email, password)
			navigate(from, { replace: true })
			// with `replace: true` browser history is replaced and thus
			// the login page doesn't stay in it, but is replaced by the
			// page it is navigating to.
		} catch (err) {
			if (err instanceof ApiError && err.status === 401) {
				setError('Invalid email or password.')
			} else {
				setError(
					err instanceof Error ? err.message : 'Login failed.',
				)
			}
		} finally {
			setIsSubmitting(false)
		}
	}

	return (
		<section className="mx-auto max-w-sm px-4 py-16">
			<h1 className="mb-6 text-2xl font-bold">Log in</h1>

			{error && (
				<p className="mb-4 rounded-md bg-primary/10 px-3 py-2 text-sm text-primary">
					{error}
				</p>
			)}

			<form onSubmit={handleSubmit} className="flex flex-col gap-4">
				<label className="flex flex-col gap-1 text-sm font-medium">
					Email
					<input
						type="email"
						required
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						className="rounded-md border border-input bg-surface px-3 py-2"
					/>
				</label>

				<label className="flex flex-col gap-1 text-sm font-medium">
					Password
					<input
						type="password"
						required
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						className="rounded-md border border-input bg-surface px-3 py-2"
					/>
				</label>

				<button
					type="submit"
					disabled={isSubmitting}
					className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover transition-colors disabled:opacity-60"
				>
					{isSubmitting ? 'Logging in…' : 'Log in'}
				</button>
			</form>

			<p className="mt-4 text-center text-sm text-muted">
				Don&apos;t have an account yet?{' '}
				<Link
					to="/signup"
					// pass `from` value to the state of the`signup` page
					state={{ from }}
					className="font-medium text-accent hover:text-accent-hover"
				>
					Sign up
				</Link>
			</p>
		</section>
	)
}
