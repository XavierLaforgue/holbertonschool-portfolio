/**
 * Shared TypeScript types / interfaces.
 *
 * Re-export domain types from here so consumers can write:
 *   import type { User } from '@/types'
 */

export interface User {
	id: string
	name: string
	email: string
	avatarUrl?: string
}

/* ── Recipes ────────────────────────────────────────────── */

/** Shape returned by /api/recipes/recipe_models/ */
export interface Recipe {
	id: string
	title: string
	anime_custom: string
	description: string
	portions: number
	preparation_time_minutes: number
	published_at: string
	created_at: string
	updated_at: string
	difficulty: string   // UUID → Difficulty
	status: string       // UUID → Status
	author: string       // UUID → User
}

/** Shape returned by /api/recipes/difficulty_models/ */
export interface Difficulty {
	id: string
	label: string
	value: number
	created_at: string
	updated_at: string
}

/* ── Auth ───────────────────────────────────────────────── */

export interface AuthContextType {
	/** The current user, or null if not logged in */
	user: User | null
	/** True while we're checking localStorage / fetching the user on app load */
	isLoading: boolean
	/** Call after a successful login — stores token + sets user */
	login: (token: string, user: User) => void
	/** Clear token + user */
	logout: () => void
}

/* --- Styling --- */

export interface ItadakimasuProps {
	whichMargin?: string
	repCount?: number
}
