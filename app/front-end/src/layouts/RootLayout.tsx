import { Outlet } from 'react-router-dom'
import Header from '@/components/Header.tsx'
import Footer from '@/components/Footer.tsx'

/**
 * Root layout — wraps every route.
 * <Outlet /> renders the matched child route.
 */
export default function RootLayout() {
	return (
		<div className="flex min-h-screen flex-col">
			<Header />

			<main className="flex-1">
				<Outlet />
			</main>

			<footer className="border-t border-border py-6 text-center text-sm text-muted">
				<Footer />
			</footer>
		</div>
	)
}
