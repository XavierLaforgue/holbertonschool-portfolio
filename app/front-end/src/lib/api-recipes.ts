import type { Recipe, RecipeDetail, RecipeWrite } from '../types'
import { apiFetch } from './api'

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
