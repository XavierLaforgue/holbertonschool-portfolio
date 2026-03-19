/** Wrappers around fetch requests to the backend API
 *
 * Base URL is read from VITE_API_BASE_URL (set in .env.local).
 * All helpers return typed JSON or throw errors on non-2xx responses.
 *
 * Authentication relies on cookies set by the backend. The frontend
 * should never read or write token cookies directly so as to prepare
 * for httpOnly cookies migration. Every request uses
 * `credentials: 'include'` so the browser sends cookies automatically.
 *
 * On a 401 the wrapper tries to refresh the access token once via
 * POST /api/token/refresh/ and retries the original request.
 */

// In development, set to the backend URL (e.g., http://localhost:8000).
// In production behind a reverse proxy, set to "" (empty string) so
// requests go to the same origin and the proxy forwards them.
export const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '') as string

if (import.meta.env.VITE_API_BASE_URL === undefined) {
	throw new Error(
		'VITE_API_BASE_URL is not defined. ' +
		'Copy .env.example into .env.local and set it ' +
		'(use "" for same-origin / reverse-proxy deployments).',
	)
}

// Use a single `Promise` for token-refresh requests so only a single
// one may be done at a time. Use case: multiple clicks on a protected
// action that results in a 401 Forbidden response and then could
// generate an equal number of refresh requests.
let refreshPromise: Promise<boolean> | null = null

/** Token refresh request
 *
 * Sends cookies to token refresh endpoint and responds whether a new
 * access token was issued (set in cookies).
 */
async function refreshAccessToken(): Promise<boolean> {
	try {
		const res = await fetch(`${API_BASE_URL}/api/token/refresh/`, {
			method: 'POST',
			credentials: 'include',
		})
		return res.ok
	} catch {
		return false
	}
}

/** Fetch wrapper
 *
 * Expects relative path (it pre-appends the BASE_URL) and optional
 * initialization options (an object with optional headers, body, ...)
 */
export async function apiFetch<T>(
	path: string,
	init?: RequestInit,
): Promise<T> {
	const url = `${API_BASE_URL}${path}`

	const doFetch = () => fetch(url, {
			...init,
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				...(init?.headers as Record<string, string>),
			},
		})

	let res = await doFetch()

	// If 401 (Unauthorized), try a single token refresh.
	if (res.status === 401) {
		// If no refresh request in process, `refreshPromise` is null
		// by default and it may proceed to actually perform the
		// refresh request. The async request returns a promise, which
		// then blocks any other `apiFetch` calls from fulfilling this
		// condition and performing the request again.
		if (!refreshPromise) {
			refreshPromise = refreshAccessToken().finally(() => {
				refreshPromise = null
			})
		}
		// Previous conditional, if entered, is executed asynchronously and it
		// is waited upon below to set `refreshed` with the return
		// value of `refreshAccessToken()` (boolean for success or failure).
		const refreshed = await refreshPromise
		if (refreshed) {
			// if refreshed, then re-try fetch with new access token.
			res = await doFetch()
		}
	}

	// request failure again or not 401: throw error
	if (!res.ok) {
		// on error (res.ok=false), the response may not be json,
		// therefore `.text()` is safer.
		const body = await res.text().catch(() => '')
		throw new ApiError(res.status, res.statusText, url, body)
	}

	// 204 (No Content): no response body. Return undefined as T: `T`
	// is the generic type, meaning whatever type the calling function expected.
	if (res.status === 204) return undefined as T

	return res.json() as Promise<T>
}


/* TODO: for httpOnly migration I should delete this function
 * Client-side cookie cleanup, fallback when the current
 * regular-cookies `logout` endpoint fails.  Once cookies are httpOnly the
 * browser won't allow this.
 */
export function clearTokensFallback(): void {
	document.cookie = 'access_token=; Max-Age=0; path=/'
	document.cookie = 'refresh_token=; Max-Age=0; path=/'
}

/** Error class
 *
 * Custom error class for the API responses. It extends regular
 * Typescript's `Error` class and adds some fields.
 */
export class ApiError extends Error {
	// declare two new fields for an Error class:
	public status: number
	public body: string

	constructor(
		status: number,
		statusText: string,
		url: string,
		body: string,
	) {
		// Set custom error message
		super(`API ${status}: ${statusText} — ${url}`)
		// Set name of the error so it is easily identifiable
		this.name = 'ApiError'
		// Stores request status and body on the instance (url and
		// statusText are not stored). Possible since they were
		// declared as fields above.
		this.status = status
		this.body = body
	}
}
