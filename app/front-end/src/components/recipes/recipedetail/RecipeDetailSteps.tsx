import StepCard from '@/components/recipes/StepCard'
import type { Step } from '@/types'

type RecipeDetailStepsProps = {
	steps: Step[]
	completedSteps: Set<string>
	onToggle: (stepId: string) => void
}

export default function RecipeDetailSteps({
	steps,
	completedSteps,
	onToggle,
}: RecipeDetailStepsProps) {
	if (steps.length === 0) return null

	return (
		<section className="mt-10">
			<h2 className="mb-4 text-xl font-bold">Steps</h2>
			<ol className="space-y-4">
				{steps.map((step) => (
					<StepCard
						key={step.id}
						step={step}
						done={completedSteps.has(step.id)}
						onToggle={onToggle}
					/>
				))}
			</ol>
		</section>
	)
}
