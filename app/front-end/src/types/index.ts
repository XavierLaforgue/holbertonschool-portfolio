/**
 * Shared TypeScript types / interfaces.
 *
 * Re-export domain types from here so consumers can write:
 *   import type { User } from '@/types'
 */

// TODO figure out how to use OpenAPI Schema for automatic typing.
export interface User {
	id: string
	username?: string
	email: string
	avatarUrl?: string
	display_name?: string
	first_name: string
	last_name: string
}

// -------------- Profiles------------------------

export interface ProfileSummary {
	id: string
	display_name: string
}

// ---------- Recipes ---------------------------------

/** Compact shape returned by GET /api/recipes/recipe_models/ (list). */
export interface Recipe {
	id: string
	title: string
	anime_custom: string
	description: string
	portions: number
	estimated_time_minutes: number
	published_at: string
	created_at: string
	updated_at: string
	difficulty: string   // UUID → Difficulty
	status: string       // UUID → RecipeStatus
	author: string       // UUID → Profile
	main_photo: string | null
}

/** Shape returned by /api/recipes/difficulty_models/ */
export interface Difficulty {
	id: string
	label: string
	value: number
	created_at: string
	updated_at: string
}

export interface RecipeStatus {
	id: string
	value: string
	created_at: string
	updated_at: string
}

export interface Step {
	id: string
	number: number
	description: string
	duration: string | null   // "HH:MM:SS" or null
	recipe: string
	created_at: string
	updated_at: string
}

export interface RecipePhoto {
	id: string
	image: string            // absolute URL
	position: number
	recipe: string
	created_at: string
	updated_at: string
}

export interface UnitKind {
	id: string
	label: string
	descriptive_name: string
}

export interface Unit {
	id: string
	name: string
	symbol: string
	kind: UnitKind
	created_at: string
	updated_at: string
}

export interface Ingredient {
	id: string
	name: string
	allowed_unit_kinds: UnitKind[]
	created_at: string
	updated_at: string
}

export interface RecipeIngredient {
	id: string
	ingredient: Ingredient
	quantity: number
	unit: Unit
	recipe: string
	created_at: string
	updated_at: string
}

/** Full shape returned by GET /api/recipes/recipe_models/{id}/ (retrieve). */
export interface RecipeDetail {
	id: string
	title: string
	anime_custom: string
	description: string
	portions: number
	estimated_time_minutes: number
	published_at: string
	created_at: string
	updated_at: string
	author: ProfileSummary
	difficulty: { label: string }
	status: RecipeStatus
	steps: Step[]
	ingredients: RecipeIngredient[]
	photos: RecipePhoto[]
}

//---------------- Auth------------------------------------

export interface AuthContextType {
	// The current user, or null if not logged in
	user: User | null
	// True while fetching (mostly)
	isLoading: boolean
	// sets user in the context
	login: (email: string, password: string) => Promise<void>
	signup: (
		email: string,
		password: string,
		firstName?: string,
		lastName?: string,
	) => Promise<void>
	// requests backend to remove cookies and cleares them if backend
	// call fails
	// TODO: update logout to not try to touch the cookies when they
	// will be httpOnly
	logout: () => Promise<void>
}

/* --- Styling --- */

export interface ItadakimasuProps {
	whichMargin?: string
	repCount?: number
}
