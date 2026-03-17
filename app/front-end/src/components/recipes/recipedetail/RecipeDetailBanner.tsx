type RecipeDetailBannerProps = {
	isAuthor: boolean
	statusValue: string
}

export default function RecipeDetailBanner({
	isAuthor,
	statusValue,
}: RecipeDetailBannerProps) {
	if (!isAuthor || statusValue === 'Published') return null

	return (
		<div className="mb-6 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3 text-sm text-blue-800 dark:border-blue-800 dark:bg-blue-950/30 dark:text-blue-300">
			This recipe is {statusValue === 'Draft' ? 'a draft' : 'marked as ready'} and is not visible to others.
		</div>
	)
}
