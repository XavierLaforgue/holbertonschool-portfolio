import { useState } from 'react'
import type { RecipePhoto } from '@/types'

type RecipeDetailHeroProps = {
	photos: RecipePhoto[]
	title: string
}

export default function RecipeDetailHero({
	photos,
	title,
}: RecipeDetailHeroProps) {
	const sorted = [...photos].sort((a, b) => a.position - b.position)
	const [index, setIndex] = useState(0)
	const total = sorted.length

	if (total === 0) {
		return (
			<div className="mb-6 flex h-64 items-center justify-center rounded-xl bg-linear-to-br from-primary/20 to-accent/20 md:h-80">
				<span className="text-4xl text-muted/40">🍜</span>
			</div>
		)
	}

	const current = sorted[index]

	return (
		<div className="group relative mb-6 h-64 overflow-hidden rounded-xl md:h-80">
			<img
				src={current.image}
				alt={`${title} — photo ${index + 1} of ${total}`}
				className="h-full w-full object-cover"
			/>

			{/* Counter badge */}
			{total > 1 && (
				<span className="absolute top-3 right-3 rounded-full bg-black/60 px-2.5 py-0.5 text-xs font-medium text-white">
					{index + 1}/{total}
				</span>
			)}

			{/* Left arrow */}
			{index > 0 && (
				<button
					onClick={() => setIndex(index - 1)}
					className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white opacity-0 transition-opacity hover:bg-black/70 group-hover:opacity-100 cursor-pointer"
					aria-label="Previous photo"
				>
					&#9664;
				</button>
			)}

			{/* Right arrow */}
			{index < total - 1 && (
				<button
					onClick={() => setIndex(index + 1)}
					className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-black/50 p-2 text-white opacity-0 transition-opacity hover:bg-black/70 group-hover:opacity-100 cursor-pointer"
					aria-label="Next photo"
				>
					&#9654;
				</button>
			)}
		</div>
	)
}
