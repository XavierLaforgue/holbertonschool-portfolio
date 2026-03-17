import { apiFetch } from './api'

export async function apiCreateIngredient(name: string): Promise<{ id: string; name: string }> {
	return apiFetch<{ id: string; name: string }>('/api/ingredients/ingredient_models/', {
		method: 'POST',
		body: JSON.stringify({ name }),
	})
}

export async function apiAddRecipeIngredient(data: {
	recipe: string
	ingredient: string
	unit: string
	quantity: number
}): Promise<unknown> {
	return apiFetch('/api/ingredients/recipeingredient_models/', {
		method: 'POST',
		body: JSON.stringify(data),
	})
}

export async function apiDeleteRecipeIngredient(id: string): Promise<void> {
	return apiFetch<void>(`/api/ingredients/recipeingredient_models/${id}/`, {
		method: 'DELETE',
	})
}
