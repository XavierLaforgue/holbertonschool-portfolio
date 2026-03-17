import type { Step } from '@/types'
import { apiFetch } from './api'

export async function apiCreateStep(
	recipeId: string,
	data: { number: number; description: string; duration?: string },
): Promise<Step> {
	return apiFetch<Step>(`/api/recipes/${recipeId}/steps/`, {
		method: 'POST',
		body: JSON.stringify(data),
	})
}

export async function apiUpdateStep(
	recipeId: string,
	stepId: string,
	data: Partial<{ description: string; duration: string | null }>,
): Promise<Step> {
	return apiFetch<Step>(`/api/recipes/${recipeId}/steps/${stepId}/`, {
		method: 'PATCH',
		body: JSON.stringify(data),
	})
}

export async function apiDeleteStep(
	recipeId: string,
	stepId: string,
): Promise<void> {
	return apiFetch<void>(`/api/recipes/${recipeId}/steps/${stepId}/`, {
		method: 'DELETE',
	})
}

export async function apiSwapSteps(
	recipeId: string,
	stepA: { id: string; number: number },
	stepB: { id: string; number: number },
): Promise<Step[]> {
	return apiFetch<Step[]>(`/api/recipes/${recipeId}/steps/`, {
		method: 'PATCH',
		body: JSON.stringify({ swap: [stepA, stepB] }),
	})
}
