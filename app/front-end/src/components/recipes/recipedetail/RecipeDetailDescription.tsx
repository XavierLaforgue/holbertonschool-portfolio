type RecipeDetailDescriptionProps = {
	description: string | null
}

export default function RecipeDetailDescription({
	description,
}: RecipeDetailDescriptionProps) {
	if (!description) return null

	return (
		<p className="mt-6 leading-relaxed text-foreground/90">
			{description}
		</p>
	)
}
