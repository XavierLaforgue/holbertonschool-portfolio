import type { User } from '../types'
import { apiFetch } from './api'

export async function apiLogin(email: string, password: string): Promise<void> {
	await apiFetch('/api/token/', {
		method: 'POST',
		body: JSON.stringify({ email, password }),
	})
}

export async function apiSignup(
	email: string,
	password: string,
	firstName?: string,  // Maybe I'll include it in the form later
	lastName?: string,  // Maybe I'll include it in the form later
): Promise<User> {
	return apiFetch<User>('/api/accounts/user_models/', {
		method: 'POST',
		body: JSON.stringify({
			email,
			password,
			...(firstName && { first_name: firstName }),
			...(lastName && { last_name: lastName }),
		}),
	})
}

export async function apiFetchMe(): Promise<User> {
	return apiFetch<User>('/api/me/')
}

export async function apiLogout(): Promise<void> {
	await apiFetch('/api/token/logout/', { method: 'POST' })
}
