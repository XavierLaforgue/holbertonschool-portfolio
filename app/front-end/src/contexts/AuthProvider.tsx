import { useState, useEffect, type ReactNode } from 'react'
import type { User } from '@/types'
import { AuthContext, TOKEN_KEY } from '@/contexts/AuthContext'

/**
 * AuthProvider — wrap your app with this so any component can call useAuth().
 *
 * How it works:
 * 1. On mount, checks localStorage for a saved JWT token.
 * 2. If found, calls your API to fetch the user profile.
 * 3. If the token is invalid/expired, clears it silently.
 * 4. login() / logout() update both state and localStorage.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
	const [user, setUser] = useState<User | null>(null)
	const [isLoading, setIsLoading] = useState(() => {
        // Initialize loading state based on whether a token exists
        return !!localStorage.getItem(TOKEN_KEY)
    })

	// On app load: check if we have a saved token and fetch user
	useEffect(() => {
		const token = localStorage.getItem(TOKEN_KEY)

		if (!token) {
			return
		}

		// TODO: Replace with your real API call
		// Example: GET /api/auth/me with the token in the Authorization header
		fetchCurrentUser(token)
			.then((user) => setUser(user))
			.catch(() => localStorage.removeItem(TOKEN_KEY)) // token expired/invalid
			.finally(() => setIsLoading(false))
	}, [])

	const login = (token: string, user: User) => {
		localStorage.setItem(TOKEN_KEY, token)
		setUser(user)
	}

	const logout = () => {
		localStorage.removeItem(TOKEN_KEY)
		setUser(null)
	}

	return (
		<AuthContext.Provider value={{ user, isLoading, login, logout }}>
			{children}
		</AuthContext.Provider>
	)
}

/**
 * TODO: Replace this with a real API call.
 *
 * This is a placeholder that simulates fetching the current user
 * from your backend using the stored JWT token.
 *
 * Real implementation would look like:
 *
 *   async function fetchCurrentUser(token: string): Promise<User> {
 *     const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/auth/me`, {
 *       headers: { Authorization: `Bearer ${token}` },
 *     })
 *     if (!res.ok) throw new Error('Invalid token')
 *     return res.json()
 *   }
 */
async function fetchCurrentUser(_token: string): Promise<User> {
	// Simulate API delay
	await new Promise((resolve) => setTimeout(resolve, 100))
	// For now, return a fake user so you can test the flow
	return {
		id: '1',
		name: 'Xavier',
		email: 'xavier@example.com',
	}
}
