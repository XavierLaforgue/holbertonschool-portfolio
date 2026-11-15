import { Link } from 'react-router-dom'

export default function Footer() {
	return (
		<>
			&copy; {new Date().getFullYear()} animize_eat
			{' · '}
			<Link to="/legal" className="underline hover:text-foreground">
				Legal notice and privacy
			</Link>
		</>
	)
}
