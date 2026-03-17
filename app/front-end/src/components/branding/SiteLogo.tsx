import { Link } from 'react-router-dom'
import logo from '@/assets/logo.png'

export default function SiteLogo() {
	return (
		<Link to="/" className="flex items-center gap-2">
			<img src={logo} alt="animize_eat logo" className="h-14 w-14" />
			<span className="text-lg font-bold text-primary-hover hover:text-primary">animize_eat</span>
		</Link>
	)
}