import { useState, type SubmitEvent } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useNavigate, useLocation, Link } from 'react-router-dom'

export default function SignUpPage() {
	const { signup } = useAuth()
	const navigate = useNavigate()
	const location = useLocation()  // allows to acess current pathname
	const [firstName, setFirstName] = useState('')
	const [lastName, setLastName] = useState('')
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState<string | null>(null)
	const [isSubmitting, setIsSubmitting] = useState(false)
	// We arrive here from a page that set their location in the state
	// as the value with key `from`.
	// We recover that state at the authentication-related pages (login/signup)
	const authState = location.state as { from?: string } | null
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
			await signup(email, password, firstName || undefined,
				lastName || undefined)
			navigate(from, { replace: true })
		} catch (err) {
			setError(
				err instanceof Error ? err.message : 'Sign-up failed.',
			)
		} finally {
			setIsSubmitting(false)
		}
	}

	return (
		<section className="mx-auto max-w-sm px-4 py-16">
			<h1 className="mb-6 text-2xl font-bold">Sign up</h1>

			{error && (
				<p className="mb-4 rounded-md bg-primary/10 px-3 py-2 text-sm text-primary">
					{error}
				</p>
			)}

			<form onSubmit={handleSubmit} className="flex flex-col gap-4">
				<div className="grid grid-cols-2 gap-3">
					<label className="flex flex-col gap-1 text-sm font-medium">
						First name
						<input
							type="text"
							value={firstName}
							onChange={(e) => setFirstName(e.target.value)}
							className="rounded-md border border-input bg-surface px-3 py-2"
						/>
					</label>

					<label className="flex flex-col gap-1 text-sm font-medium">
						Last name
						<input
							type="text"
							value={lastName}
							onChange={(e) => setLastName(e.target.value)}
							className="rounded-md border border-input bg-surface px-3 py-2"
						/>
					</label>
				</div>

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
					{isSubmitting ? 'Creating account…' : 'Sign up'}
				</button>
			</form>

			<p className="mt-4 text-center text-sm text-muted">
				Already have an account?{' '}
				<Link
					to="/login"
					// pass `from` value to the state of the `/login` page
					state={{ from }}
					className="font-medium text-accent hover:text-accent-hover"
				>
					Log in
				</Link>
			</p>
		</section>
	)
}
