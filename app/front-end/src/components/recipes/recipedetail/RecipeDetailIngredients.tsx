import type { RecipeIngredient } from '@/types'

type RecipeDetailIngredientsProps = {
	ingredients: RecipeIngredient[]
}

export default function RecipeDetailIngredients({
	ingredients,
}: RecipeDetailIngredientsProps) {
	if (ingredients.length === 0) return null

	return (
		<section className="mt-10">
			<h2 className="mb-4 text-xl font-bold">Ingredients</h2>
			<div className="rounded-xl border border-border bg-surface p-4">
				<ul className="divide-y divide-border">
					{ingredients.map((ri) => (
						<li key={ri.id} className="flex items-center justify-between py-2 text-sm">
							<span className="font-medium text-foreground">{ri.ingredient.name}</span>
							<span className="text-muted">{ri.quantity} {ri.unit.symbol}</span>
						</li>
					))}
				</ul>
			</div>
		</section>
	)
}
