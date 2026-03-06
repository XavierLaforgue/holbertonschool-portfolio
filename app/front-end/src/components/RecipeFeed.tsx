import { useCallback, useEffect, useState } from 'react'
import { apiFetch } from '@/lib/api'
import RecipeCard from '@/components/RecipeCard'
import type { Recipe, Difficulty } from '@/types'

export default function RecipeFeed() {
	const [recipes, setRecipes] = useState<Recipe[]>([])
	const [difficulties, setDifficulties] = useState<Map<string, Difficulty>>(
		new Map(),
	)
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	const loadRecipes = useCallback(async () => {
		setIsLoading(true)
		setError(null)

		try {
			const [recipesData, diffData] = await Promise.all([
				apiFetch<Recipe[]>('/api/recipes/recipe_models/'),
				apiFetch<Difficulty[]>('/api/recipes/difficulty_models/'),
			])

			setRecipes(recipesData)

			const map = new Map<string, Difficulty>()
			for (const d of diffData) map.set(d.id, d)
			setDifficulties(map)
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load recipes')
		} finally {
			setIsLoading(false)
		}
	}, [])

	useEffect(() => {
		loadRecipes()
	}, [loadRecipes])

	return (
		<section
			id="featured-recipes"
			className="container mx-auto px-4 py-12 md:py-16"
		>
			{/* Header row */}
			<div className="mb-8 flex items-end justify-between">
				<div>
					<h2 className="text-2xl font-bold md:text-3xl">Latest Recipes</h2>
					<p className="mt-1 text-sm text-muted">
						Fresh from the community kitchen
					</p>
				</div>

				<button
					onClick={loadRecipes}
					disabled={isLoading}
					className="flex items-center gap-1.5 rounded-md border border-border bg-surface px-3 py-1.5 text-sm font-medium text-muted transition-colors hover:bg-surface-hover hover:text-foreground disabled:opacity-50"
					aria-label="Refresh recipes"
				>
					{/* Refresh icon */}
					<svg
						xmlns="http://www.w3.org/2000/svg"
						viewBox="0 0 20 20"
						fill="currentColor"
						className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`}
					>
						<path
							fillRule="evenodd"
							d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.451a.75.75 0 0 0 0-1.5H4.5a.75.75 0 0 0-.75.75v3.75a.75.75 0 0 0 1.5 0v-2.136l.312.311a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.388l-.013.024Zm-10.624-2.85a5.5 5.5 0 0 1 9.201-2.465l.312.31H12.75a.75.75 0 0 0 0 1.5h3.75a.75.75 0 0 0 .75-.75V3.419a.75.75 0 0 0-1.5 0v2.137l-.312-.311A7 7 0 0 0 3.226 8.382a.75.75 0 0 0 1.449.388l.013-.024Z"
							clipRule="evenodd"
						/>
					</svg>
					Refresh
				</button>
			</div>

			{/* Loading skeleton */}
			{isLoading && (
				<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{Array.from({ length: 6 }).map((_, i) => (
						<div
							key={i}
							className="animate-pulse rounded-xl border border-border bg-surface"
						>
							<div className="h-40 rounded-t-xl bg-surface-hover" />
							<div className="space-y-3 p-4">
								<div className="h-5 w-3/4 rounded bg-surface-hover" />
								<div className="h-4 w-full rounded bg-surface-hover" />
								<div className="h-4 w-5/6 rounded bg-surface-hover" />
								<div className="flex gap-3 pt-2">
									<div className="h-3 w-14 rounded bg-surface-hover" />
									<div className="h-3 w-16 rounded bg-surface-hover" />
								</div>
							</div>
						</div>
					))}
				</div>
			)}

			{/* Error state */}
			{error && (
				<div className="rounded-lg border border-primary/30 bg-primary/5 px-6 py-10 text-center">
					<p className="text-lg font-semibold text-primary">
						Oops — couldn't load recipes
					</p>
					<p className="mt-1 text-sm text-muted">{error}</p>
				</div>
			)}

			{/* Empty state */}
			{!isLoading && !error && recipes.length === 0 && (
				<div className="rounded-lg border border-border bg-surface px-6 py-16 text-center">
					<p className="text-5xl">🍙</p>
					<p className="mt-4 text-lg font-semibold">No recipes yet!</p>
					<p className="mt-1 text-sm text-muted">
						Be the first to share an anime-inspired dish.
					</p>
				</div>
			)}

			{/* Recipe grid */}
			{!isLoading && !error && recipes.length > 0 && (
				<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{recipes.map((recipe) => (
						<RecipeCard
							key={recipe.id}
							recipe={recipe}
							difficulty={difficulties.get(recipe.difficulty)}
						/>
					))}
				</div>
			)}
		</section>
	)
}
