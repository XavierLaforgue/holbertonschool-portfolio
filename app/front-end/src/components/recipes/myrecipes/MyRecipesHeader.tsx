import RefreshButton from '@/components/recipes/RefreshButton'

type MyRecipesHeaderProps = {
	isLoading: boolean
	onRefresh: () => void
}

export default function MyRecipesHeader({
	isLoading,
	onRefresh,
}: MyRecipesHeaderProps) {
	return (
		<div className="mb-8 flex items-end justify-between">
			<div>
				<h1 className="text-2xl font-bold md:text-3xl">My Recipes</h1>
				<p className="mt-1 text-sm text-muted">
					Your saved and created recipes
				</p>
			</div>

			<RefreshButton
				loadRecipes={onRefresh}
				isLoading={isLoading}
			/>
		</div>
	)
}
