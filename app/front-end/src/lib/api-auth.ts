import type { User } from '../types'
import { apiFetch } from './api'

export async function apiLogin(email: string, password: string): Promise<void> {
	await apiFetch('/api/token/', {
		method: 'POST',
		body: JSON.stringify({ email, password }),
	})
}

// Sign-up asks only for what the account needs (RGPD minimization).
export async function apiSignup(email: string, password: string): Promise<User> {
	return apiFetch<User>('/api/accounts/user_models/', {
		method: 'POST',
		body: JSON.stringify({ email, password }),
	})
}

export async function apiFetchMe(): Promise<User> {
	return apiFetch<User>('/api/me/')
}

export async function apiLogout(): Promise<void> {
	await apiFetch('/api/token/logout/', { method: 'POST' })
}

/** Delete the account for good (the back-end also deletes the cookies). */
export async function apiDeleteAccount(userId: string): Promise<void> {
	await apiFetch(`/api/accounts/user_models/${userId}/`, { method: 'DELETE' })
}
