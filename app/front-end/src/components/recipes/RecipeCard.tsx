import { Link } from 'react-router-dom'
import type { Recipe } from '@/types'

// ------- Difficulty badge---------------------------------

const DIFFICULTY_COLORS: Record<string, string> = {
	easy: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
	medium:
		'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
	hard: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
	expert: 'bg-gray-900 text-gray-100 dark:bg-gray-700 dark:text-gray-100',
}

function difficultyBadge(label: string) {
	const key = label.toLowerCase()
	const color = DIFFICULTY_COLORS[key] ?? 'bg-surface-hover text-muted'
	return (
		<span
			className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-semibold ${color}`}
		>
			{label}
		</span>
	)
}

// ------------ Time formatter ---------------------------------

function formatTime(mins: number): string {
	if (mins < 60) return `${mins} min`
	const h = Math.floor(mins / 60)
	const m = mins % 60
	return m ? `${h}h ${m}min` : `${h}h`
}

// --------- Placeholder image--------------------------

function PlaceholderImage() {
	return (
		<div className="flex h-full w-full items-center justify-center bg-linear-to-br from-primary/20 to-accent/20">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				width="24"
				height="24"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				strokeWidth="2"
				strokeLinecap="round"
				strokeLinejoin="round"
				className="lucide lucide-cooking-pot h-10 w-10 text-muted/40"
			>
				<path d="M2 12h20"/>
				<path d="M20 12v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8"/>
				<path d="m4 8 16-4"/>
				<path d="m8.86 6.78-.45-1.81a2 2 0 0 1 1.45-2.43l1.94-.48a2 2 0 0 1 2.43 1.46l.45 1.8"/>
			</svg>
		</div>
	)
}

// ----------- Card ---------------------------------

interface RecipeCardProps {
	recipe: Recipe
}

export default function RecipeCard({ recipe }: RecipeCardProps) {
	const publishedDate = recipe.published_at
		? new Date(recipe.published_at).toLocaleDateString(undefined, {
				year: 'numeric',
				month: 'short',
				day: 'numeric',
		  })
		: null

	return (
		<Link
			to={`/recipes/${recipe.id}`}
			className="group flex cursor-pointer flex-col overflow-hidden rounded-xl border border-border bg-surface shadow-sm transition-shadow hover:shadow-md"
		>
			{/* Image area */}
			<div className="relative h-40 overflow-hidden">
				{recipe.main_photo ? (
					<img
						src={recipe.main_photo}
						alt={recipe.title}
						className="h-full w-full object-cover transition-transform group-hover:scale-105"
					/>
				) : (
					<PlaceholderImage />
				)}

				{/* Anime source tag */}
				{recipe.anime_custom && (
					<span className="absolute top-2 right-2 rounded-md bg-black/40 px-2 py-0.5 text-xs font-medium text-white backdrop-blur-sm">
						{recipe.anime_custom}
					</span>
				)}
			</div>

			<div className="flex flex-1 flex-col gap-1.5 p-4">
				{/* Title */}
				<h3 className="text-lg font-bold leading-tight text-foreground group-hover:text-primary transition-colors line-clamp-2">
					{recipe.title || <span className="italic text-muted">Untitled</span>}
				</h3>

				{/* Author */}
				<p className="text-xs text-muted">by {recipe.author.display_name}</p>

				{/* Description */}
				<p className="flex-1 text-sm leading-relaxed text-muted line-clamp-3 mt-0.5">
					{recipe.description}
				</p>

				{/* Meta row */}
				<div className="mt-auto flex flex-wrap items-center gap-3 pt-3 border-t border-border text-xs text-muted">
					{/* Prep time */}
					{recipe.estimated_time_minutes != null && recipe.estimated_time_minutes > 0 && (
						<span className="flex items-center gap-1" title="Preparation time">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								viewBox="0 0 20 20"
								fill="currentColor"
								className="h-3.5 w-3.5"
							>
								<path
									fillRule="evenodd"
									d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm.75-13a.75.75 0 0 0-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 0 0 0-1.5h-3.25V5Z"
									clipRule="evenodd"
								/>
							</svg>
							{formatTime(recipe.estimated_time_minutes)}
						</span>
					)}

					{/* Portions */}
					<span className="flex items-center gap-1" title="Portions">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
							className="h-3.5 w-3.5"
						>
							<path d="M7 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM14.5 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1.615 16.428a1.224 1.224 0 0 1-.569-1.175 6.002 6.002 0 0 1 11.908 0c.058.467-.172.92-.57 1.174A9.953 9.953 0 0 1 7 18a9.953 9.953 0 0 1-5.385-1.572ZM14.5 16h-.106c.07-.297.088-.611.048-.933a7.47 7.47 0 0 0-1.588-3.755 4.502 4.502 0 0 1 5.874 2.636.818.818 0 0 1-.36.98A7.465 7.465 0 0 1 14.5 16Z" />
						</svg>
						{recipe.portions} {recipe.portions === 1 ? 'serving' : 'servings'}
					</span>

					{/* Difficulty badge */}
					{recipe.difficulty && difficultyBadge(recipe.difficulty.label)}

					{/* Published date — pushed to the right */}
					{publishedDate && (
						<time className="ml-auto" dateTime={recipe.published_at ?? ''}>
							{publishedDate}
						</time>
					)}
				</div>
			</div>
		</Link>
	)
}
