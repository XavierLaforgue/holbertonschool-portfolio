import { useRouteError, isRouteErrorResponse, Link } from 'react-router-dom'

export default function ErrorPage() {
	const error = useRouteError()

	let title = 'Something went wrong'
	let message = 'An unexpected error occurred.'

	if (isRouteErrorResponse(error)) {
		title = `${error.status} ${error.statusText}`
		message = error.data?.message || message
	} else if (error instanceof Error) {
		message = error.message
	}

	return (
		<div className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
			<h1 className="text-4xl font-bold">{title}</h1>
			<p className="mt-4 text-muted">{message}</p>
			<Link
				to="/"
				className="mt-8 rounded-lg bg-secondary px-6 py-3 text-sm font-medium text-secondary-fg transition-colors hover:bg-secondary-hover"
			>
				Go home
			</Link>
		</div>
	)
}
