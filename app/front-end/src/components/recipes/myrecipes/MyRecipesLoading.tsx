import type { RecipeGroupConfig } from '@/components/recipes/myrecipes/MyRecipesGroups'

type MyRecipesLoadingProps = {
	groups: RecipeGroupConfig[]
}

export default function MyRecipesLoading({ groups }: MyRecipesLoadingProps) {
	return (
		<div className="space-y-10">
			{groups.map((group) => (
				<div key={group.key} className="space-y-4">
					<div className="flex items-center justify-between">
						<div className="h-5 w-32 rounded bg-surface-hover" />
						<div className="h-4 w-16 rounded bg-surface-hover" />
					</div>
					<div className="overflow-x-auto">
						<div className="flex gap-4 pb-2">
							{Array.from({ length: 3 }).map((_, i) => (
								<div
									key={i}
									className="w-72 flex-none animate-pulse rounded-xl border border-border bg-surface"
								>
									<div className="h-36 rounded-t-xl bg-surface-hover" />
									<div className="space-y-3 p-4">
										<div className="h-5 w-3/4 rounded bg-surface-hover" />
										<div className="h-3 w-1/2 rounded bg-surface-hover" />
										<div className="h-4 w-full rounded bg-surface-hover" />
									</div>
								</div>
							))}
						</div>
					</div>
				</div>
			))}
		</div>
	)
}
