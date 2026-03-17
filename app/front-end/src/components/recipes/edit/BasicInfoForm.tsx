import type { Difficulty } from '@/types'

interface BasicInfoFormProps {
	title: string
	animeCustom: string
	description: string
	difficultyId: string
	portions: number
	estimatedTime: number
	difficulties: Difficulty[]
	onChange: (field: string, value: string | number) => void
}

const inputClass =
	'w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50'

export default function BasicInfoForm({
	title,
	animeCustom,
	description,
	difficultyId,
	portions,
	estimatedTime,
	difficulties,
	onChange,
}: BasicInfoFormProps) {
	return (
		<section className="space-y-4">
			<h2 className="text-lg font-semibold">Basic info</h2>

			<div>
				<label className="mb-1 block text-sm font-medium text-muted">Title</label>
				<input
					type="text"
					value={title}
					onChange={(e) => onChange('title', e.target.value)}
					placeholder="Recipe title"
					className={inputClass}
				/>
			</div>

			<div>
				<label className="mb-1 block text-sm font-medium text-muted">Anime source</label>
				<input
					type="text"
					value={animeCustom}
					onChange={(e) => onChange('animeCustom', e.target.value)}
					placeholder="e.g. Shokugeki no Soma"
					className={inputClass}
				/>
			</div>

			<div>
				<label className="mb-1 block text-sm font-medium text-muted">Description</label>
				<textarea
					rows={5}
					value={description}
					onChange={(e) => onChange('description', e.target.value)}
					placeholder="Short description (optional)"
					className={inputClass}
				/>
			</div>

			<div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
				<div>
					<label className="mb-1 block text-sm font-medium text-muted">Difficulty</label>
					<select
						value={difficultyId}
						onChange={(e) => onChange('difficultyId', e.target.value)}
						className={inputClass}
					>
						{/* <option value="">— none —</option> */}
						{difficulties.map((option_of_difficulty) => (
							<option key={option_of_difficulty.id}
								value={option_of_difficulty.id}>
									{option_of_difficulty.label}
							</option>
						))}
					</select>
				</div>

				<div>
					<label className="mb-1 block text-sm font-medium text-muted">Portions</label>
					<input
						type="number"
						min={1}
						value={portions}
						onChange={(e) => onChange('portions', Number(e.target.value))}
						className={inputClass}
					/>
				</div>

				<div>
					<label className="mb-1 block text-sm font-medium text-muted">Time (min)</label>
					<input
						type="number"
						min={0}
						value={estimatedTime}
						onChange={(e) => onChange('estimatedTime', Number(e.target.value))}
						className={inputClass}
					/>
				</div>
			</div>
		</section>
	)
}
