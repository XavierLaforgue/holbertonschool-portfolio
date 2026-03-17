import type { RecipePhoto } from '../types'
import { API_BASE_URL, ApiError, apiFetch } from './api'

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

	const url = `${API_BASE_URL}/api/recipes/${recipeId}/photos/`
	const res = await fetch(url, {
		method: 'POST',
		credentials: 'include',
		body: form,
		// Do NOT set Content-Type — browser sets it with the multipart boundary
	})
	if (!res.ok) {
		const body = await res.text().catch(() => '')
		throw new ApiError(res.status, res.statusText, url, body)
	}
	return res.json()
}

export async function apiDeletePhoto(
	recipeId: string,
	photoId: string,
): Promise<void> {
	return apiFetch<void>(`/api/recipes/${recipeId}/photos/${photoId}/`, {
		method: 'DELETE',
	})
}
