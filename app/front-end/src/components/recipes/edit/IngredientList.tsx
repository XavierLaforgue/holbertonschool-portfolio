import type { IngredientWrite } from '@/types'

interface Unit {
	id: string
	name: string
	symbol: string
}

interface IngredientListProps {
	ingredients: IngredientWrite[]
	units: Unit[]
	onChange: (ingredients: IngredientWrite[]) => void
}

const inputClass =
	'rounded-lg border border-border bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50'

export default function IngredientList({
	ingredients,
	units,
	onChange,
}: IngredientListProps) {
	function updateRow(index: number, patch: Partial<IngredientWrite>) {
		const updated = ingredients.map((row, i) =>
			i === index ? { ...row, ...patch } : row,
		)
		onChange(updated)
	}

	function removeRow(index: number) {
		onChange(ingredients.filter((_, i) => i !== index))
	}

	function addRow() {
		onChange([
			...ingredients,
			{ ingredient_name: '', quantity: 1, unit: units[0]?.id ?? '' },
		])
	}

	return (
		<section>
			<h2 className="mb-4 text-lg font-semibold">Ingredients</h2>

			{ingredients.length > 0 && (
				<div className="mb-4 space-y-2">
					{ingredients.map((row, i) => (
						<div key={i} className="flex flex-wrap items-center gap-2">
							<input
								type="text"
								value={row.ingredient_name}
								onChange={(e) => updateRow(i, { ingredient_name: e.target.value })}
								placeholder="Ingredient name"
								className={`min-w-0 flex-1 ${inputClass}`}
							/>
							<input
								type="number"
								min={0}
								step="1"
								value={row.quantity}
								onChange={(e) => updateRow(i, { quantity: Number(e.target.value) })}
								className={`w-20 ${inputClass}`}
							/>
							<select
								value={row.unit}
								onChange={(e) => updateRow(i, { unit: e.target.value })}
								className={inputClass}
							>
								{units.map((u) => (
									<option key={u.id} value={u.id}>
										{u.symbol} ({u.name})
									</option>
								))}
							</select>
							<button
								onClick={() => removeRow(i)}
								className="text-muted hover:text-primary transition-colors px-1"
								aria-label="Remove ingredient"
							>
								&times;
							</button>
						</div>
					))}
				</div>
			)}

			<button
				onClick={addRow}
				className="rounded-lg border border-dashed border-border px-4 py-2 text-sm font-medium text-muted hover:bg-surface-hover transition-colors cursor-pointer"
			>
				+ Add ingredient
			</button>
		</section>
	)
}
