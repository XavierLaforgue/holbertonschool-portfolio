import { useContext } from 'react'
import { AuthContext } from '@/contexts/AuthContext'

/**
 * Access auth state from any component.
 *
 * Usage:
 *   const { user, isLoading, login, logout } = useAuth()
 *
 *   if (isLoading) return <Spinner />
 *   if (!user) return <LoginButton />
 *   return <p>Hello {user.name}</p>
 */
export function useAuth() {
	const context = useContext(AuthContext)

	if (context === undefined) {
		throw new Error('useAuth must be used within an <AuthProvider>')
	}

	return context
}
