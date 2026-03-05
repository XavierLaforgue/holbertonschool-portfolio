import { createBrowserRouter } from 'react-router-dom'
import RootLayout from '@/layouts/RootLayout'
import HomePage from '@/pages/HomePage'
import NotFoundPage from '@/pages/NotFoundPage'
import ErrorPage from '@/pages/ErrorPage'
import LoginPage from '@/pages/LoginPage'

/**
 * Application router.
 *
 * Add new routes as objects inside the `children` array of the root layout.
 * Lazy-load heavy pages with:
 *   { path: '/about', lazy: () => import('@/pages/AboutPage') }
 */
const router = createBrowserRouter([
	{
		path: '/',
		element: <RootLayout />,
		errorElement: <ErrorPage />,
		children: [
			{ index: true, element: <HomePage /> },
			{ path: 'login', element: <LoginPage /> },
			{ path: '*', element: <NotFoundPage /> },
		],
	},
])

export default router
