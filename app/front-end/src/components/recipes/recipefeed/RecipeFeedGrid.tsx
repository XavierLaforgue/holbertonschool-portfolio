import RecipeCard from '@/components/recipes/RecipeCard'
import type { Recipe } from '@/types'

type RecipeFeedGridProps = {
	recipes: Recipe[]
}

export default function RecipeFeedGrid({ recipes }: RecipeFeedGridProps) {
	return (
		<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
			{recipes.map((recipe) => (
				<RecipeCard key={recipe.id} recipe={recipe} />
			))}
		</div>
	)
}
