import { useState, type SubmitEvent } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { useNavigate, Link } from 'react-router-dom'

export default function LoginPage() {
	const { login } = useAuth()
	const navigate = useNavigate()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')

	const handleSubmit = (e: SubmitEvent) => {
		e.preventDefault()

		// TODO: Replace with real API call
		// For now, simulate a successful login
		login('fake-jwt-token', {
			id: '1',
			name: 'Xavier',
			email,
		})

		navigate('/')
	}

	return (
		<section className="mx-auto max-w-sm px-4 py-16">
			<h1 className="mb-6 text-2xl font-bold">Log in</h1>

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
					className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover transition-colors"
				>
					Log in
				</button>
			</form>

			<p className="mt-4 text-center text-sm text-muted">
				Don&apos;t have an account yet?{' '}
				<Link to="/signup" className="font-medium text-accent hover:text-accent-hover">
					Sign up
				</Link>
			</p>
		</section>
	)
}
