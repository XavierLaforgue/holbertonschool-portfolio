/**
 * Thin wrapper around fetch for the backend API.
 *
 * Base URL is read from VITE_API_BASE_URL (set in .env.local).
 * All helpers return typed JSON or throw on non-2xx responses.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string

if (!API_BASE_URL) {
	throw new Error(
		'VITE_API_BASE_URL is not defined. ' +
		'Copy .env.example → .env.local and set it.',
	)
}

/** Generic fetch wrapper that prepends the base URL and parses JSON. */
export async function apiFetch<T>(
	path: string,
	init?: RequestInit,
): Promise<T> {
	const url = `${API_BASE_URL}${path}`

	const res = await fetch(url, {
		headers: {
			'Content-Type': 'application/json',
			...(init?.headers as Record<string, string>),
		},
		...init,
	})

	if (!res.ok) {
		throw new Error(`API ${res.status}: ${res.statusText} — ${url}`)
	}

	return res.json() as Promise<T>
}
