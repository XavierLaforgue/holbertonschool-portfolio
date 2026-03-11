import { createBrowserRouter } from 'react-router-dom'
import RootLayout from '@/layouts/RootLayout'
import HomePage from '@/pages/HomePage'
import NotFoundPage from '@/pages/NotFoundPage'
import ErrorPage from '@/pages/ErrorPage'
import LoginPage from '@/pages/LoginPage'
import SignUpPage from '@/pages/SignUpPage'
import RecipeDetailPage from '@/pages/RecipeDetailPage'
import RecipeEditPage from '@/pages/RecipeEditPage'
import MyRecipesPage from '@/pages/MyRecipesPage'

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
			{ path: 'signup', element: <SignUpPage /> },
			// Edit must come before :id to avoid ":id" matching "create"
			{ path: 'recipes/:id/edit', element: <RecipeEditPage /> },
			{ path: 'recipes/:id', element: <RecipeDetailPage /> },
			{ path: 'recipes/', element: <MyRecipesPage /> },
			{ path: '*', element: <NotFoundPage /> },
		],
	},
])

export default router
