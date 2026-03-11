import RecipeCard from '@/components/recipes/RecipeCard'
import type { Recipe } from '@/types'

export type RecipeGroupKey = 'draft' | 'ready' | 'published' | 'saved'

export type GroupedRecipes = Record<RecipeGroupKey, Recipe[]>

export type RecipeGroupConfig = {
	key: RecipeGroupKey
	title: string
	empty: string
}

type MyRecipesGroupsProps = {
	groups: RecipeGroupConfig[]
	data: GroupedRecipes
	openGroups: Record<RecipeGroupKey, boolean>
	onToggle: (key: RecipeGroupKey) => void
}

export default function MyRecipesGroups({
	groups,
	data,
	openGroups,
	onToggle,
}: MyRecipesGroupsProps) {
	return (
		<div className="space-y-10">
			{groups.map((group) => {
				const recipes = data[group.key]
				const isOpen = openGroups[group.key]
				const sectionId = `group-${group.key}`

				return (
					<section key={group.key} className="space-y-4">
						<button
							type="button"
							onClick={() => onToggle(group.key)}
							aria-expanded={isOpen}
							aria-controls={sectionId}
							className="flex w-full items-center justify-between rounded-lg border border-border bg-surface px-4 py-3 text-left transition-colors hover:bg-surface-hover"
						>
							<div className="flex items-center gap-3">
								<h2 className="text-lg font-semibold">{group.title}</h2>
								<span className="rounded-full bg-surface-hover px-2 py-0.5 text-xs text-muted">
									{recipes.length}
								</span>
							</div>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								className={`h-5 w-5 transition-transform ${isOpen ? 'rotate-180' : ''}`}
								aria-hidden="true"
							>
								<path
									fillRule="evenodd"
									d="M5.23 7.21a.75.75 0 0 1 1.06.02L10 10.94l3.71-3.71a.75.75 0 1 1 1.06 1.06l-4.24 4.24a.75.75 0 0 1-1.06 0L5.21 8.29a.75.75 0 0 1 .02-1.08Z"
									clipRule="evenodd"
								/>
							</svg>
						</button>

						{isOpen && (
							<div id={sectionId} className="space-y-3">
								{recipes.length === 0 ? (
									<p className="text-sm text-muted">{group.empty}</p>
								) : (
									<div className="overflow-x-auto">
										<div className="flex gap-4 pb-2">
											{recipes.map((recipe) => (
												<div
													key={recipe.id}
													className="w-72 flex-none"
												>
													<RecipeCard recipe={recipe} />
												</div>
											))}
										</div>
									</div>
								)}
							</div>
						)}
					</section>
				)
			})}
		</div>
	)
}
