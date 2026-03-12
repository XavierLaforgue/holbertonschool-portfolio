import { useState } from 'react'
import type { Step } from '@/types'

interface StepListProps {
	steps: Step[]
	onAdd: (description: string, duration: string) => Promise<void>
	onDelete: (step: Step) => void
	onSwap: (stepA: Step, stepB: Step) => void
	onBlur: (step: Step, field: 'description' | 'duration', value: string) => void
}

const inputClass =
	'rounded-md border border-border bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50'

export default function StepList({
	steps,
	onAdd,
	onDelete,
	onSwap,
	onBlur,
}: StepListProps) {
	const [desc, setDesc] = useState('')
	const [duration, setDuration] = useState('')
	const [adding, setAdding] = useState(false)

	const sorted = [...steps].sort((a, b) => a.number - b.number)

	async function handleAdd() {
		if (!desc.trim()) return
		setAdding(true)
		try {
			await onAdd(desc.trim(), duration)
			setDesc('')
			setDuration('')
		} finally {
			setAdding(false)
		}
	}

	return (
		<section>
			<h2 className="mb-4 text-lg font-semibold">Steps</h2>

			{/* Existing steps */}
			{sorted.length > 0 && (
				<ol className="mb-4 space-y-3">
					{sorted.map((step, idx) => (
						<li key={step.id} className="flex gap-3 rounded-xl border border-border bg-surface p-3">
							{/* Reorder arrows */}
							<div className="flex flex-col gap-1 pt-0.5">
								<button
									disabled={idx === 0}
									onClick={() => onSwap(step, sorted[idx - 1])}
									className="text-muted hover:text-foreground disabled:opacity-20 transition-colors"
									aria-label="Move step up"
								>
									&#9650;
								</button>
								<button
									disabled={idx === sorted.length - 1}
									onClick={() => onSwap(step, sorted[idx + 1])}
									className="text-muted hover:text-foreground disabled:opacity-20 transition-colors"
									aria-label="Move step down"
								>
									&#9660;
								</button>
							</div>

							{/* Step number */}
							<span className="mt-1 w-6 shrink-0 text-center text-sm font-bold text-muted">
								{step.number}.
							</span>

							{/* Editable content */}
							<div className="flex-1 space-y-2">
								<textarea
									defaultValue={step.description}
									rows={2}
									onBlur={(e) => onBlur(step, 'description', e.target.value)}
									className="w-full rounded-md border border-border bg-transparent px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
								/>
								<input
									type="text"
									defaultValue={step.duration ?? ''}
									placeholder="Duration HH:MM:SS (optional)"
									onBlur={(e) => onBlur(step, 'duration', e.target.value)}
									className="w-40 rounded-md border border-border bg-transparent px-2 py-1 text-xs text-muted focus:outline-none focus:ring-2 focus:ring-primary/50"
								/>
							</div>

							{/* Delete */}
							<button
								onClick={() => onDelete(step)}
								className="self-start text-muted hover:text-primary transition-colors"
								aria-label="Delete step"
							>
								&times;
							</button>
						</li>
					))}
				</ol>
			)}

			{/* Add step row */}
			<div className="space-y-2 rounded-xl border border-dashed border-border p-3">
				<textarea
					rows={2}
					value={desc}
					onChange={(e) => setDesc(e.target.value)}
					placeholder="Step description…"
					className={`w-full ${inputClass}`}
				/>
				<div className="flex items-center gap-2">
					<input
						type="text"
						value={duration}
						onChange={(e) => setDuration(e.target.value)}
						placeholder="Duration HH:MM:SS (optional)"
						className={`flex-1 text-muted ${inputClass}`}
					/>
					<button
						onClick={handleAdd}
						disabled={adding || !desc.trim()}
						className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover disabled:opacity-50 transition-colors"
					>
						{adding ? 'Adding…' : 'Add step'}
					</button>
				</div>
			</div>
		</section>
	)
}
