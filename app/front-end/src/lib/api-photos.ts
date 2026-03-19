import type { RecipePhoto } from '../types'
import { apiFetch } from './api'

/**
 * Upload a photo for a recipe.
 * Uses FormData so the browser sets multipart/form-data content-type automatically.
 */
export async function apiUploadPhoto(
	recipeId: string,
	file: File,
	position: number,
): Promise<RecipePhoto> {
	const form = new FormData()
	form.append('image', file)
	form.append('position', String(position))

	return apiFetch<RecipePhoto>(`/api/recipes/${recipeId}/photos/`, {
		method: 'POST',
		body: form,
		// Do NOT set Content-Type — apiFetch skips it for FormData,
		// letting the browser set multipart/form-data with boundary
	})
}

export async function apiDeletePhoto(
	recipeId: string,
	photoId: string,
): Promise<void> {
	return apiFetch<void>(`/api/recipes/${recipeId}/photos/${photoId}/`, {
		method: 'DELETE',
	})
}
