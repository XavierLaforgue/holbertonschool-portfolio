import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useRecipeDetail, useStepCompletion, useRecipeSaveCopy, useRecipeStatus } from '../hooks/useRecipeDetail'
import { DIFF_COLORS, formatTime } from '../utils/recipe'
import RecipeDetailActions from '../components/recipes/recipedetail/RecipeDetailActions'
import RecipeDetailBanner from '../components/recipes/recipedetail/RecipeDetailBanner'
import RecipeDetailDescription from '../components/recipes/recipedetail/RecipeDetailDescription'
import RecipeDetailGallery from '../components/recipes/recipedetail/RecipeDetailGallery'
import RecipeDetailHero from '../components/recipes/recipedetail/RecipeDetailHero'
import RecipeDetailIngredients from '../components/recipes/recipedetail/RecipeDetailIngredients'
import RecipeDetailMeta from '../components/recipes/recipedetail/RecipeDetailMeta'
import RecipeDetailSteps from '../components/recipes/recipedetail/RecipeDetailSteps'
import RecipeDetailTitle from '../components/recipes/recipedetail/RecipeDetailTitle'

export default function RecipeDetailPage() {
	const { id } = useParams<{ id: string }>()
	const navigate = useNavigate()
	const { user } = useAuth()
	const { recipe, setRecipe, isLoading, error } = useRecipeDetail(id)
	const { completedSteps, toggleStep } = useStepCompletion()
	const { saveState, handleSaveCopy } = useRecipeSaveCopy(recipe)
	const { statusLoading, statusError, handleStatusChange } = useRecipeStatus(recipe, setRecipe)

	/* ------------ Loading state -------------------------------- */

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

	/* ------------ Error state ---------------------------------- */

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
	const isAuthor = !!(user && recipe && user.profile_id === recipe.author.id)
	const statusValue = recipe.status.value

	const mainPhoto = recipe.photos.find((p) => p.position === 1)
	const galleryPhotos = recipe.photos.filter((p) => p.position !== 1)
	const sortedSteps = [...recipe.steps].sort((a, b) => a.number - b.number)
	const difficultyKey = recipe.difficulty.label.toLowerCase()
	const difficultyColor = DIFF_COLORS[difficultyKey] ?? 'bg-surface-hover text-muted'

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
				difficultyColor={difficultyColor}
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
