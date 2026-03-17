import type { RecipeDetail } from '@/types'

type RecipeDetailTitleProps = {
	recipe: RecipeDetail
}

export default function RecipeDetailTitle({ recipe }: RecipeDetailTitleProps) {
	return (
		<>
			<h1 className="text-3xl font-bold md:text-4xl">
				{recipe.title || <span className="italic text-muted">Untitled recipe</span>}
			</h1>

			<div className="mt-2 flex flex-wrap items-center gap-3 text-sm text-muted">
				<span>by {recipe.author.display_name}</span>
				{recipe.anime_custom && (
					<>
						<span className="text-border">·</span>
						<span className="italic">{recipe.anime_custom}</span>
					</>
				)}
				{recipe.published_at && (
					<>
						<span className="text-border">·</span>
						<time dateTime={recipe.published_at}>
							{new Date(recipe.published_at).toLocaleDateString(undefined, {
								year: 'numeric',
								month: 'long',
								day: 'numeric',
							})}
						</time>
					</>
				)}
			</div>
		</>
	)
}
