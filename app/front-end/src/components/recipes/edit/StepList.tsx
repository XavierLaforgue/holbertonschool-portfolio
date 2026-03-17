import type { StepWrite } from '@/types'

interface StepListProps {
	steps: StepWrite[]
	onChange: (steps: StepWrite[]) => void
}

const inputClass =
	'rounded-lg border border-border bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50'

function parseDuration(duration: string | null): { h: number; m: number; s: number } {
	if (!duration) return { h: 0, m: 0, s: 0 }
	const parts = duration.split(':')
	return {
		h: parseInt(parts[0] ?? '0', 10) || 0,
		m: parseInt(parts[1] ?? '0', 10) || 0,
		s: parseInt(parts[2] ?? '0', 10) || 0,
	}
}

function formatDuration(h: number, m: number, s: number): string | null {
	if (h === 0 && m === 0 && s === 0) return null
	const pad = (n: number) => String(n).padStart(2, '0')
	return `${pad(h)}:${pad(m)}:${pad(s)}`
}

export default function StepList({ steps, onChange }: StepListProps) {
	function updateRow(index: number, patch: Partial<StepWrite>) {
		const updated = steps.map((row, i) =>
			i === index ? { ...row, ...patch } : row,
		)
		onChange(updated)
	}

	function removeRow(index: number) {
		// Remove and renumber
		const updated = steps
			.filter((_, i) => i !== index)
			.map((step, i) => ({ ...step, number: i + 1 }))
		onChange(updated)
	}

	function addRow() {
		onChange([
			...steps,
			{ number: steps.length + 1, description: '', duration: null },
		])
	}

	function swapRows(indexA: number, indexB: number) {
		const updated = [...steps]
		const temp = updated[indexA]
		updated[indexA] = { ...updated[indexB], number: indexA + 1 }
		updated[indexB] = { ...temp, number: indexB + 1 }
		onChange(updated)
	}

	function handleDurationPart(
		index: number,
		part: 'h' | 'm' | 's',
		value: number,
	) {
		const current = parseDuration(steps[index].duration)
		current[part] = Math.max(0, value)
		updateRow(index, { duration: formatDuration(current.h, current.m, current.s) })
	}

	return (
		<section>
			<h2 className="mb-4 text-lg font-semibold">Steps</h2>

			{steps.length > 0 && (
				<ol className="mb-4 space-y-3">
					{steps.map((step, idx) => {
						const { h, m, s } = parseDuration(step.duration)
						return (
							<li key={idx} className="flex gap-3 rounded-xl border border-border bg-surface p-3">
								{/* Reorder arrows */}
								<div className="flex flex-col gap-1 pt-0.5">
									<button
										disabled={idx === 0}
										onClick={() => swapRows(idx, idx - 1)}
										className="text-muted hover:text-foreground disabled:opacity-20 transition-colors cursor-pointer"
										aria-label="Move step up"
									>
										&#9650;
									</button>
									<button
										disabled={idx === steps.length - 1}
										onClick={() => swapRows(idx, idx + 1)}
										className="text-muted hover:text-foreground disabled:opacity-20 transition-colors cursor-pointer"
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
										value={step.description}
										rows={2}
										onChange={(e) => updateRow(idx, { description: e.target.value })}
										placeholder="Step description..."
										className="w-full rounded-md border border-border bg-transparent px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
									/>
									<div className="flex items-center gap-1 text-xs text-muted">
										<span>Duration:</span>
										<input
											type="number"
											min={0}
											value={h}
											onChange={(e) => handleDurationPart(idx, 'h', parseInt(e.target.value, 10) || 0)}
											className={`w-14 text-center ${inputClass} text-xs`}
											aria-label="Hours"
										/>
										<span>h</span>
										<input
											type="number"
											min={0}
											max={59}
											value={m}
											onChange={(e) => handleDurationPart(idx, 'm', parseInt(e.target.value, 10) || 0)}
											className={`w-14 text-center ${inputClass} text-xs`}
											aria-label="Minutes"
										/>
										<span>m</span>
										<input
											type="number"
											min={0}
											max={59}
											value={s}
											onChange={(e) => handleDurationPart(idx, 's', parseInt(e.target.value, 10) || 0)}
											className={`w-14 text-center ${inputClass} text-xs`}
											aria-label="Seconds"
										/>
										<span>s</span>
									</div>
								</div>

								{/* Delete */}
								<button
									onClick={() => removeRow(idx)}
									className="self-start text-muted hover:text-primary transition-colors cursor-pointer"
									aria-label="Delete step"
								>
									&times;
								</button>
							</li>
						)
					})}
				</ol>
			)}

			<button
				onClick={addRow}
				className="rounded-lg border border-dashed border-border px-4 py-2 text-sm font-medium text-muted hover:bg-surface-hover transition-colors cursor-pointer"
			>
				+ Add step
			</button>
		</section>
	)
}
