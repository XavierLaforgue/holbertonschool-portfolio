import type { RecipeDetail } from '@/types'

type RecipeDetailMetaProps = {
	timeLabel: string | null
	portions: number
	difficulty: RecipeDetail['difficulty']
	difficultyColor: string
}

export default function RecipeDetailMeta({
	timeLabel,
	portions,
	difficulty,
	difficultyColor,
}: RecipeDetailMetaProps) {
	return (
		<div className="mt-4 flex flex-wrap items-center gap-4 text-sm text-muted">
			{timeLabel && <span>{timeLabel}</span>}
			<span>
				{portions} {portions === 1 ? 'serving' : 'servings'}
			</span>
			{difficulty && (
				<span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold ${difficultyColor}`}>
					{difficulty.label}
				</span>
			)}
		</div>
	)
}
