import type { RecipePhoto } from '@/types'

type RecipeDetailHeroProps = {
	mainPhoto?: RecipePhoto
	title: string
}

export default function RecipeDetailHero({
	mainPhoto,
	title,
}: RecipeDetailHeroProps) {
	if (mainPhoto) {
		return (
			<img
				src={mainPhoto.image}
				alt={title}
				className="mb-6 h-64 w-full rounded-xl object-cover md:h-80"
			/>
		)
	}

	return (
		<div className="mb-6 flex h-64 items-center justify-center rounded-xl bg-linear-to-br from-primary/20 to-accent/20 md:h-80">
			<span className="text-4xl text-muted/40">🍜</span>
		</div>
	)
}
