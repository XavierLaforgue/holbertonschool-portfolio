import { Link } from 'react-router-dom'

export default function NotFoundPage() {
	return (
		<section className="container mx-auto flex flex-col items-center px-4 py-32 text-center">
			<h1 className="text-6xl font-bold">404</h1>
			<p className="mt-4 text-lg text-muted">
				Page not found.
			</p>
			<Link
				to="/"
				className="mt-8 rounded-lg bg-secondary px-6 py-3 text-sm font-medium text-secondary-fg transition-colors hover:bg-secondary-hover"
			>
				Go home
			</Link>
		</section>
	)
}
