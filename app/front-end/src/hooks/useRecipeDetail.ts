import { useCallback, useEffect, useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { apiFetch, ApiError } from '../lib/api'
import { apiSaveRecipe, apiSetRecipeStatus } from '../lib/api-recipes'
import { useAuth } from '../hooks/useAuth'
import type { RecipeDetail } from '../types'

/* ---- Fetch a single recipe by id -------------------------------- */

export function useRecipeDetail(id: string | undefined) {
	const [recipe, setRecipe] = useState<RecipeDetail | null>(null)
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	const loadRecipe = useCallback(async () => {
		if (!id) return
		setIsLoading(true)
		setError(null)
		try {
			const data = await apiFetch<RecipeDetail>(`/api/recipes/recipe_models/${id}/`)
			setRecipe(data)
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load recipe')
		} finally {
			setIsLoading(false)
		}
	}, [id])

	useEffect(() => { loadRecipe() }, [loadRecipe])

	return { recipe, setRecipe, isLoading, error }
}

/* ---- Step completion toggle ------------------------------------- */

export function useStepCompletion() {
	const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set())

	const toggleStep = useCallback((stepId: string) => {
		setCompletedSteps((prev) => {
			const next = new Set(prev)
			if (next.has(stepId)) next.delete(stepId)
			else next.add(stepId)
			return next
		})
	}, [])

	return { completedSteps, toggleStep }
}

/* ---- Save a copy of someone else's recipe ----------------------- */

export function useRecipeSaveCopy(recipe: RecipeDetail | null) {
	const { user } = useAuth()
	const navigate = useNavigate()
	const location = useLocation()
	const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')

	const handleSaveCopy = useCallback(async () => {
		if (!recipe) return
		if (!user) {
			navigate('/login', { state: { from: location.pathname } })
			return
		}
		setSaveState('saving')
		try {
			await apiSaveRecipe({
				title: recipe.title,
				anime_custom: recipe.anime_custom,
				description: recipe.description,
				difficulty: recipe.difficulty?.id,
				portions: recipe.portions,
				estimated_time_minutes: recipe.estimated_time_minutes,
				status: recipe.status.id,
				original_recipe: recipe.id,
				original_author: recipe.author.id,
			})
			setSaveState('saved')
		} catch {
			setSaveState('error')
		}
	}, [recipe, user, navigate, location.pathname])

	return { saveState, handleSaveCopy }
}

/* ---- Author status actions (draft ↔ published) ------------------ */

export function useRecipeStatus(
	recipe: RecipeDetail | null,
	setRecipe: React.Dispatch<React.SetStateAction<RecipeDetail | null>>,
) {
	const [statusLoading, setStatusLoading] = useState(false)
	const [statusError, setStatusError] = useState<string | null>(null)

	const handleStatusChange = useCallback(async (newValue: string) => {
		if (!recipe) return
		setStatusLoading(true)
		setStatusError(null)
		try {
			const updated = await apiSetRecipeStatus(recipe.id, newValue)
			setRecipe(updated)
		} catch (err) {
			if (err instanceof ApiError) {
				try {
					const parsed = JSON.parse(err.body)
					const messages = parsed.details ?? parsed.detail
					setStatusError(
						Array.isArray(messages) ? messages.join('\n') : String(messages),
					)
				} catch {
					setStatusError(err.body)
				}
			} else {
				setStatusError(err instanceof Error ? err.message : 'Failed to update status')
			}
		} finally {
			setStatusLoading(false)
		}
	}, [recipe, setRecipe])

	return { statusLoading, statusError, handleStatusChange }
}
