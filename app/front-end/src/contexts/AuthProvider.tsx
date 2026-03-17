import { useState, useEffect, useCallback, type ReactNode } from 'react'
import type { User } from '../types'
import { AuthContext } from '../contexts/AuthContext'
import { clearTokensFallback } from '../lib/api'
import { apiLogin, apiSignup, apiFetchMe, apiLogout } from '../lib/api-auth'

/**
 * AuthProvider: wrap app so any component can call `useAuth()`.
 *
 * How it works:
 * 1. On mount, does GET /api/accounts/me/ (with cookies).
 * 2. If the cookie is valid, sets the user. Otherwise, user stays null.
 * 3. login() / signup() / logout() update state and let the backend
 *    manage cookies via Set-Cookie headers.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
	const [user, setUser] = useState<User | null>(null)
	const [isLoading, setIsLoading] = useState(true)

	// On page load: check if we have valid tokens in the cookies vie
	// the /me endpoint
	useEffect(() => {
		apiFetchMe()
			.then(res => setUser(res))
			.catch(() => {
				// Not logged in or token expired.
				// Empty so the "error" response is treating as
				// expected/ok and not an actual error.
				// TODO: improve by defining the expected "error"
				// status codes of the response instead of considering
				// every error code as expected/OK.
				setUser(null)
			})
			.finally(() => setIsLoading(false))
	}, [])

	// Usage of useCallback(): We need login(), logout(), and signup()
	// to have stable function references across re-renders. Otherwise,
	// each time something in the context changes, e.g., `isLoading` and
	// `user` states, the three functions would be recreated.
	// This recreation would trigger re-renders of every component with
	// useEffect(()=>{}, [login, logout, or signup]). Basically, every
	// time some property of the context changes, all of them get new
	// references and every component consuming the context would be
	// re-rendered.
	
	const login = useCallback(async (email: string, password: string) => {
		await apiLogin(email, password)      // backend sets cookies
		const me = await apiFetchMe()        // send cookies to backend to get
											 //  user data back (if valid token)
		setUser(me)
	}, [])

	const signup = useCallback(
		async (
			email: string,
			password: string,
			firstName?: string,
			lastName?: string,
		) => {
			await apiSignup(email, password, firstName, lastName)
			// automatic login after registration
			await login(email, password)
		},
		[login],
	)

	const verifyAuth = useCallback(async () => {
		try {
			const me = await apiFetchMe()
			setUser(me)
			return me
		} catch {
			setUser(null)
			return null
		}
	}, [])

	const logout = useCallback(async () => {
		try {
			await apiLogout()  // backend clears cookies: pattern pre-migration 
							   // to httponly cookies
		} catch {
			// In case of failure, clear cookies from the client.
			// TODO: When using httpOnly cookies, remove this fallback entirely.
			clearTokensFallback()
		}
		setUser(null)
	}, [])

	return (
		<AuthContext.Provider value={{ user, isLoading, login, signup, verifyAuth, logout }}>
			{children}
		</AuthContext.Provider>
	)
}
