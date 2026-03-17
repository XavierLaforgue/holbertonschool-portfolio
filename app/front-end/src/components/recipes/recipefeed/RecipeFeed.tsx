import RecipeFeedEmpty from '@/components/recipes/recipefeed/RecipeFeedEmpty'
import RecipeFeedError from '@/components/recipes/recipefeed/RecipeFeedError'
import RecipeFeedGrid from '@/components/recipes/recipefeed/RecipeFeedGrid'
import RecipeFeedHeader from '@/components/recipes/recipefeed/RecipeFeedHeader'
import RecipeFeedLoading from '@/components/recipes/recipefeed/RecipeFeedLoading'
import { useRecipes } from '@/hooks/useRecipes'
import type { Recipe } from '@/types'

export default function RecipeFeed() {
	const {
		data: recipes, // destructuring, `data` from the object becomes
					   // `recipes`
		isLoading,
		error,
		loadRecipes,
	} = useRecipes<Recipe[]>('/api/recipes/recipe_models/', { initialData: [] })

	// const [recipes, setRecipes] = useState<Recipe[]>([])
	// const [isLoading, setIsLoading] = useState(true)
	// const [error, setError] = useState<string | null>(null)
	// const loadRecipes = useCallback(async () => {
	// 	setIsLoading(true)
	// 	setError(null)
	// 	try {
	// 		const data = await apiFetch<Recipe[]>('/api/recipes/recipe_models/')
	// 		setRecipes(data)
	// 	} catch (err) {
	// 		setError(err instanceof Error ? err.message : 'Failed to load recipes')
	// 	} finally {
	// 		setIsLoading(false)
	// 	}
	// }, [])
	// useEffect(() => {
	// 	loadRecipes()
	// }, [loadRecipes])

	return (
		<section
			id="featured-recipes"
			className="container mx-auto px-4 py-12 md:py-16"
		>
			<RecipeFeedHeader
				isLoading={isLoading}
				onRefresh={loadRecipes}
			/>

			{/* Loading skeleton */}
			{isLoading && <RecipeFeedLoading />}

			{/* Error state */}
			{error && <RecipeFeedError message={error} />}

			{/* Empty state */}
			{!isLoading && !error && recipes.length === 0 && <RecipeFeedEmpty />}

			{/* Recipe grid */}
			{!isLoading && !error && recipes.length > 0 && (
				<RecipeFeedGrid recipes={recipes} />
			)}
		</section>
	)
}
