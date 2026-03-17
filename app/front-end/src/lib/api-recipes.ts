import type { // Difficulty, 
	Recipe, RecipeDetail, RecipeWrite } from '../types'
import { apiFetch } from './api'

/** If not set by the api (view), then dificulty (id) would have to be provided 
 * 
 */
// let easyDifficultyIdPromise: Promise<string> | null = null

// async function getDifficultyIdByLabel(label: string): Promise<string> {
// 	const diffs = await apiFetch<Difficulty[]>('/api/recipes/difficulty_models/')
// 	const wanted = label.trim().toLowerCase()
// 	const match = diffs.find(
// 		(difficulty) => difficulty.label.trim().toLowerCase() === wanted)
// 	if (!match) {
// 		throw new Error(`Difficulty "${label}" not found in /api/recipes/difficulty_models/`)
// 	}
// 	return match.id
// }

// async function getEasyDifficultyId(): Promise<string> {
// 	if (!easyDifficultyIdPromise) {
// 		easyDifficultyIdPromise = getDifficultyIdByLabel('Easy')
// 	}
// 	return easyDifficultyIdPromise
// }

/**
 * Create a draft recipe owned by the current user.
 * The backend requires some fields (including difficulty and status), so we send defaults.
 */
// export async function apiCreateRecipe(data: Partial<RecipeWrite> = {}): Promise<Recipe> {
// 	const difficulty = data.difficulty ?? await getEasyDifficultyId()
// 	return apiFetch<Recipe>('/api/recipes/recipe_models/', {
// 		method: 'POST',
// 		body: JSON.stringify({
// 			difficulty,
// 		} satisfies RecipeWrite),
// 	})
// }

/** Create a blank draft recipe owned by the current user. */
export async function apiCreateRecipe(): Promise<Recipe> {
	return apiFetch<Recipe>('/api/recipes/recipe_models/', { method: 'POST' })
}

/** Partial-update the recipe's basic info fields. */
export async function apiUpdateRecipe(
	id: string,
	data: RecipeWrite,
): Promise<RecipeDetail> {
	return apiFetch<RecipeDetail>(`/api/recipes/recipe_models/${id}/`, {
		method: 'PATCH',
		body: JSON.stringify(data),
	})
}

/** Fetch full recipe detail. */
export async function apiFetchRecipe(id: string): Promise<RecipeDetail> {
	return apiFetch<RecipeDetail>(`/api/recipes/recipe_models/${id}/`)
}

/**
 * Change the recipe status.
 * value: "Draft" | "Ready" | "Published"
 */
export async function apiSetRecipeStatus(
	id: string,
	value: string,
): Promise<RecipeDetail> {
	return apiFetch<RecipeDetail>(`/api/recipes/recipe_models/${id}/status/`, {
		method: 'PATCH',
		body: JSON.stringify({ value }),
	})
}

/** Save a copy of a published recipe (non-author). */
export async function apiSaveRecipe(data: Record<string, unknown>): Promise<unknown> {
	return apiFetch('/api/recipes/savedrecipe_models/', {
		method: 'POST',
		body: JSON.stringify(data),
	})
}
