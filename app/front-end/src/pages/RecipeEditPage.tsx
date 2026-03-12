import { useCallback, useEffect, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import {
	apiFetchRecipe,
	apiUpdateRecipe,
	apiCreateStep,
	apiUpdateStep,
	apiDeleteStep,
	apiSwapSteps,
	apiCreateIngredient,
	apiAddRecipeIngredient,
	apiDeleteRecipeIngredient,
	apiUploadPhoto,
	apiDeletePhoto,
	apiFetch,
} from '@/lib/api'
import type { RecipeDetail, Step, RecipeIngredient, RecipePhoto, Difficulty } from '@/types'
import BasicInfoForm from '@/components/recipes/edit/BasicInfoForm'
import IngredientList from '@/components/recipes/edit/IngredientList'
import StepList from '@/components/recipes/edit/StepList'
import PhotoGrid from '@/components/recipes/edit/PhotoGrid'

interface Unit { id: string; name: string; symbol: string }

function statusBadge(value: string) {
	const colors: Record<string, string> = {
		Draft: 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
		Ready: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
		Published: 'bg-green-100 text-green-700 dark:bg-green-900/40 dark:text-green-300',
	}
	return (
		<span className={`rounded-full px-3 py-0.5 text-xs font-semibold ${colors[value] ?? colors.Draft}`}>
			{value}
		</span>
	)
}

export default function RecipeEditPage() {
	const { id } = useParams<{ id: string }>()
	const navigate = useNavigate()
	const location = useLocation()
	const { user, isLoading: authLoading } = useAuth()

	// Recipe data
	const [recipe, setRecipe] = useState<RecipeDetail | null>(null)
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	// Basic info form state
	const [title, setTitle] = useState('')
	const [animeCustom, setAnimeCustom] = useState('')
	const [description, setDescription] = useState('')
	const [difficultyId, setDifficultyId] = useState('')
	const [portions, setPortions] = useState(1)
	const [estimatedTime, setEstimatedTime] = useState(0)
	const [saving, setSaving] = useState(false)
	const [saveError, setSaveError] = useState<string | null>(null)

	// Supporting data
	const [difficulties, setDifficulties] = useState<Difficulty[]>([])
	const [units, setUnits] = useState<Unit[]>([])

	// Photo upload state (kept here because PhotoGrid's onUpload needs loadRecipe)
	const [photoUploading, setPhotoUploading] = useState(false)
	const [photoError, setPhotoError] = useState<string | null>(null)

	// ----- Auth guard --------------------------------------

	useEffect(() => {
		if (authLoading) return
		if (!user) {
			navigate('/login', { state: { from: location.pathname }, 
				replace: true })
		}
	}, [authLoading, user, navigate, location.pathname])

	// ------ Load recipe + supporting data --------------------

	const loadRecipe = useCallback(async () => {
		if (!id) return
		setIsLoading(true)
		setError(null)
		try {
			const [data, diffs, unitList] = await Promise.all([
				apiFetchRecipe(id),
				apiFetch<Difficulty[]>('/api/recipes/difficulty_models/'),
				apiFetch<Unit[]>('/api/ingredients/unit_models/'),
			])
			setRecipe(data)
			setTitle(data.title)
			setAnimeCustom(data.anime_custom)
			setDescription(data.description ?? '')
			setDifficultyId(data.difficulty?.id ?? '')
			setPortions(data.portions)
			setEstimatedTime(data.estimated_time_minutes)
			setDifficulties(diffs)
			setUnits(unitList)
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load recipe')
		} finally {
			setIsLoading(false)
		}
	}, [id])

	useEffect(() => { loadRecipe() }, [loadRecipe])

	// -----Non-author redirect ------------------------------

	useEffect(() => {
		if (recipe && user && recipe.author.id !== user.profile_id) {
			navigate(`/recipes/${id}`, { replace: true })
		}
	}, [recipe, user, id, navigate])

	// -------Handlers-------------------------------------------

	function handleBasicInfoChange(field: string, value: string | number) {
		const setters: Record<string, (v: any) => void> = {
			title: setTitle, 
			animeCustom: setAnimeCustom,
			description: setDescription,
			difficultyId: setDifficultyId,
			portions: setPortions,
			estimatedTime: setEstimatedTime,
		}
		setters[field]?.(value)
	}

	async function handleSave() {
		if (!recipe) return
		setSaving(true)
		setSaveError(null)
		try {
			await apiUpdateRecipe(recipe.id, {
				title, anime_custom: animeCustom, description,
				difficulty: difficultyId || undefined,
				portions, estimated_time_minutes: estimatedTime,
			})
			navigate(`/recipes/${recipe.id}`)
		} catch (err) {
			setSaveError(err instanceof Error ? err.message : 'Failed to save')
		} finally {
			setSaving(false)
		}
	}

	async function handleAddIngredient(name: string, qty: number, unitId: string) {
		if (!recipe) return
		const ing = await apiCreateIngredient(name)
		await apiAddRecipeIngredient({ recipe: recipe.id, ingredient: ing.id, unit: unitId, quantity: qty })
		await loadRecipe()
	}

	function handleDeleteIngredient(ri: RecipeIngredient) {
		apiDeleteRecipeIngredient(ri.id)
		setRecipe((prev) => prev ? { ...prev, ingredients: prev.ingredients.filter((i) => i.id !== ri.id) } : prev)
	}

	async function handleAddStep(desc: string, duration: string) {
		if (!recipe) return
		const nextNumber = recipe.steps.length > 0 ? Math.max(...recipe.steps.map((s) => s.number)) + 1 : 1
		await apiCreateStep(recipe.id, { number: nextNumber, description: desc, ...(duration ? { duration } : {}) })
		await loadRecipe()
	}

	function handleDeleteStep(step: Step) {
		apiDeleteStep(recipe!.id, step.id)
		setRecipe((prev) => prev ? { ...prev, steps: prev.steps.filter((s) => s.id !== step.id) } : prev)
	}

	async function handleSwapSteps(stepA: Step, stepB: Step) {
		if (!recipe) return
		const updated = await apiSwapSteps(recipe.id, { id: stepA.id, number: stepA.number }, { id: stepB.id, number: stepB.number })
		setRecipe((prev) => (prev ? { ...prev, steps: updated } : prev))
	}

	function handleStepBlur(step: Step, field: 'description' | 'duration', value: string) {
		if (!recipe) return
		apiUpdateStep(recipe.id, step.id, field === 'duration' ? { duration: value || null } : { description: value })
	}

	async function handlePhotoUpload(file: File, position: number) {
		if (!recipe) return
		setPhotoUploading(true)
		setPhotoError(null)
		try {
			await apiUploadPhoto(recipe.id, file, position)
			await loadRecipe()
		} catch (err) {
			setPhotoError(err instanceof Error ? err.message : 'Upload failed')
		} finally {
			setPhotoUploading(false)
		}
	}

	function handleDeletePhoto(photo: RecipePhoto) {
		apiDeletePhoto(recipe!.id, photo.id)
		setRecipe((prev) => prev ? { ...prev, photos: prev.photos.filter((p) => p.id !== photo.id) } : prev)
	}

	// ------ Render states --------------------------------------

	if (authLoading || isLoading) {
		return (
			<div className="container mx-auto max-w-3xl px-4 py-16">
				<div className="animate-pulse space-y-6">
					<div className="h-8 w-1/3 rounded bg-surface-hover" />
					<div className="h-12 rounded bg-surface-hover" />
					<div className="h-12 rounded bg-surface-hover" />
					<div className="h-32 rounded bg-surface-hover" />
				</div>
			</div>
		)
	}

	if (error || !recipe) {
		return (
			<div className="container mx-auto max-w-3xl px-4 py-16 text-center">
				<p className="text-lg font-semibold text-primary">{error ?? 'Recipe not found'}</p>
				<button onClick={() => navigate(-1)} className="mt-4 rounded-md bg-secondary px-4 py-2 text-sm font-medium transition-colors hover:bg-secondary-hover">
					Go back
				</button>
			</div>
		)
	}

	return (
		<div className="container mx-auto max-w-3xl px-4 py-8 md:py-12">

			{/* Header */}
			<div className="mb-8 flex items-center justify-between gap-4">
				<h1 className="text-2xl font-bold">Edit Recipe</h1>
				{statusBadge(recipe.status.value)}
			</div>

			{/* Basic info */}
			<BasicInfoForm
				title={title} animeCustom={animeCustom} description={description}
				difficultyId={difficultyId} portions={portions} estimatedTime={estimatedTime}
				difficulties={difficulties} onChange={handleBasicInfoChange}
			/>

			<hr className="my-8 border-border" />

			{/* Ingredients */}
			<IngredientList
				ingredients={recipe.ingredients} units={units}
				onAdd={handleAddIngredient} onDelete={handleDeleteIngredient}
			/>

			<hr className="my-8 border-border" />

			{/* Steps */}
			<StepList
				steps={recipe.steps} onAdd={handleAddStep} onDelete={handleDeleteStep}
				onSwap={handleSwapSteps} onBlur={handleStepBlur}
			/>

			<hr className="my-8 border-border" />

			{/* Photos */}
			<PhotoGrid
				photos={recipe.photos} uploading={photoUploading} error={photoError}
				onUpload={handlePhotoUpload} onDelete={handleDeletePhoto}
			/>

			<hr className="my-8 border-border" />

			{/* Save / Cancel */}
			<div className="flex items-center justify-between gap-4">
				<button onClick={() => navigate(`/recipes/${recipe.id}`)} className="rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-surface-hover transition-colors">
					Cancel
				</button>
				<div className="flex items-center gap-3">
					{saveError && <p className="text-xs text-primary">{saveError}</p>}
					<button onClick={handleSave} disabled={saving} className="rounded-lg bg-primary px-6 py-2 text-sm font-semibold text-primary-fg hover:bg-primary-hover disabled:opacity-50 transition-colors">
						{saving ? 'Saving…' : 'Save'}
					</button>
				</div>
			</div>
		</div>
	)
}
