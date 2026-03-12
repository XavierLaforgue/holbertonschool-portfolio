import { useCallback, useEffect, useState } from 'react'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { apiFetch, apiSaveRecipe, apiSetRecipeStatus } from '@/lib/api'
import { useAuth } from '@/hooks/useAuth'
import RecipeDetailActions from '@/components/recipes/recipedetail/RecipeDetailActions'
import RecipeDetailBanner from '@/components/recipes/recipedetail/RecipeDetailBanner'
import RecipeDetailDescription from '@/components/recipes/recipedetail/RecipeDetailDescription'
import RecipeDetailGallery from '@/components/recipes/recipedetail/RecipeDetailGallery'
import RecipeDetailHero from '@/components/recipes/recipedetail/RecipeDetailHero'
import RecipeDetailIngredients from '@/components/recipes/recipedetail/RecipeDetailIngredients'
import RecipeDetailMeta from '@/components/recipes/recipedetail/RecipeDetailMeta'
import RecipeDetailSteps from '@/components/recipes/recipedetail/RecipeDetailSteps'
import RecipeDetailTitle from '@/components/recipes/recipedetail/RecipeDetailTitle'
import type { RecipeDetail } from '@/types'

/* ------- Helpers ------------------------------------------- */

const DIFF_COLORS: Record<string, string> = {
	easy: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
	medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
	hard: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
	expert: 'bg-gray-900 text-gray-100 dark:bg-gray-700 dark:text-gray-100',
}

function formatTime(mins: number): string {
	if (mins < 60) return `${mins} min`
	const h = Math.floor(mins / 60)
	const m = mins % 60
	return m ? `${h}h ${m}min` : `${h}h`
}

/* ---- Page --------------------------------------------------- */

export default function RecipeDetailPage() {
	const { id } = useParams<{ id: string }>()
	const navigate = useNavigate()
	const location = useLocation()
	const { user } = useAuth()

	const [recipe, setRecipe] = useState<RecipeDetail | null>(null)
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)
	const [completedSteps, setCompletedSteps] = useState<Set<string>>(new Set())
	const [saveState, setSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')
	const [statusLoading, setStatusLoading] = useState(false)
	const [statusError, setStatusError] = useState<string | null>(null)

	/* ------- Fetch recipe -------------------------------------- */

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

	/* --------- Derived state ------------------------------- */

	const isAuthor = !!(user && recipe && user.profile_id === recipe.author.id)
	const statusValue = recipe?.status.value ?? ''

	/* -------------- Step toggle ---------------------------- */

	function toggleStep(stepId: string) {
		setCompletedSteps((prev) => {
			const next = new Set(prev)
			if (next.has(stepId)) next.delete(stepId)
			else next.add(stepId)
			return next
		})
	}

	/* -------------------- Save copy (non-author) ------------------ */

	async function handleSaveCopy() {
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
	}

	/* --------- Status actions (author) --------------------- */

	async function handleStatusChange(newValue: string) {
		if (!recipe) return
		setStatusLoading(true)
		setStatusError(null)
		try {
			const updated = await apiSetRecipeStatus(recipe.id, newValue)
			setRecipe(updated)
		} catch (err) {
			setStatusError(err instanceof Error ? err.message : 'Failed to update status')
		} finally {
			setStatusLoading(false)
		}
	}

	/* ------------ Render states ---------------------------- */

	if (isLoading) {
		return (
			<div className="container mx-auto max-w-3xl px-4 py-16">
				<div className="animate-pulse space-y-6">
					<div className="h-64 rounded-xl bg-surface-hover" />
					<div className="h-8 w-2/3 rounded bg-surface-hover" />
					<div className="h-4 w-1/3 rounded bg-surface-hover" />
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

	/* ----------- Derived data ---------------------------------- */

	const mainPhoto = recipe.photos.find((p) => p.position === 1)
	const galleryPhotos = recipe.photos.filter((p) => p.position !== 1)
	const sortedSteps = [...recipe.steps].sort((a, b) => a.number - b.number)
	const diffKey = recipe.difficulty?.label.toLowerCase() ?? ''
	const diffColor = DIFF_COLORS[diffKey] ?? 'bg-surface-hover text-muted'

	return (
		<div className="container mx-auto max-w-3xl px-4 py-8 md:py-12">

			{/* Draft/Ready banner (author only) */}
			<RecipeDetailBanner
				isAuthor={isAuthor}
				statusValue={statusValue}
			/>

			{/* Hero image */}
			<RecipeDetailHero
				mainPhoto={mainPhoto}
				title={recipe.title}
			/>

			{/* Title + author */}
			<RecipeDetailTitle recipe={recipe} />

			{/* Metadata bar */}
			<RecipeDetailMeta
				timeLabel={recipe.estimated_time_minutes > 0 ? formatTime(recipe.estimated_time_minutes) : null}
				portions={recipe.portions}
				difficulty={recipe.difficulty}
				diffColor={diffColor}
			/>

			{/* Action bar */}
			<RecipeDetailActions
				isAuthor={isAuthor}
				statusValue={statusValue}
				statusLoading={statusLoading}
				statusError={statusError}
				onStatusChange={handleStatusChange}
				onEdit={() => navigate(`/recipes/${recipe.id}/edit`)}
				saveState={saveState}
				onSaveCopy={handleSaveCopy}
			/>

			{/* Description */}
			<RecipeDetailDescription description={recipe.description} />

			{/* Photo gallery */}
			<RecipeDetailGallery
				photos={galleryPhotos}
				title={recipe.title}
			/>

			{/* Ingredients */}
			<RecipeDetailIngredients ingredients={recipe.ingredients} />

			{/* Steps */}
			<RecipeDetailSteps
				steps={sortedSteps}
				completedSteps={completedSteps}
				onToggle={toggleStep}
			/>
		</div>
	)
}
