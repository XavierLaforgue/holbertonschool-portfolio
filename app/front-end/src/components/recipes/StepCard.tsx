import type { Step } from '@/types'
import StepTimer from '@/components/recipes/StepTimer'

interface StepCardProps {
	step: Step
	done: boolean
	onToggle: (stepId: string) => void
}

export default function StepCard({ step, done, onToggle }: StepCardProps) {
	return (
		<li
			className={`flex gap-4 rounded-xl border p-4 transition-colors ${
				done
					? 'border-green-300 bg-green-50 dark:border-green-800 dark:bg-green-950/30'
					: 'border-border bg-surface'
			}`}
		>
			{/* Checkbox */}
			<button
				type="button"
				onClick={() => onToggle(step.id)}
				className={`mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors ${
					done
						? 'border-green-500 bg-green-500 text-white dark:border-green-400 dark:bg-green-400 dark:text-green-950'
						: 'border-border hover:border-muted'
				}`}
				aria-label={done ? `Mark step ${step.number} incomplete` : `Mark step ${step.number} complete`}
			>
				{done && <span className="text-xs font-bold">✓</span>}
			</button>

			{/* Content */}
			<div className="flex-1">
				<p className={`text-sm leading-relaxed ${done ? 'text-muted line-through' : 'text-foreground'}`}>
					<span className="mr-2 font-bold text-muted">{step.number}.</span>
					{step.description}
				</p>

				{step.duration && (
					<div className="mt-3">
						<StepTimer duration={step.duration} />
					</div>
				)}
			</div>
		</li>
	)
}
