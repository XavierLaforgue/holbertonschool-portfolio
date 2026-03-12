import RefreshButton from '@/components/recipes/RefreshButton'

type RecipeFeedHeaderProps = {
	isLoading: boolean
	onRefresh: () => void
}

export default function RecipeFeedHeader({
	isLoading,
	onRefresh,
}: RecipeFeedHeaderProps) {
	return (
		<div className="mb-8 flex items-end justify-between">
			<div>
				<h2 className="text-2xl font-bold md:text-3xl">Featured Recipes</h2>
				<p className="mt-1 text-sm text-muted">
					Fresh from the community's kitchen
				</p>
			</div>

			<RefreshButton loadRecipes={onRefresh} isLoading={isLoading} />
		</div>
	)
}
