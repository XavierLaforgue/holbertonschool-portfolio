import { useState } from 'react'
import type { RecipeIngredient } from '@/types'

interface Unit {
	id: string
	name: string
	symbol: string
}

interface IngredientListProps {
	ingredients: RecipeIngredient[]
	units: Unit[]
	onAdd: (name: string, quantity: number, unitId: string) => Promise<void>
	onDelete: (ri: RecipeIngredient) => void
}

const inputClass =
	'rounded-lg border border-border bg-surface px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50'

export default function IngredientList({
	ingredients,
	units,
	onAdd,
	onDelete,
}: IngredientListProps) {
	const [name, setName] = useState('')
	const [qty, setQty] = useState(1)
	const [unitId, setUnitId] = useState(units[0]?.id ?? '')
	const [adding, setAdding] = useState(false)
	const [error, setError] = useState<string | null>(null)

	async function handleAdd() {
		if (!name.trim() || !unitId) return
		setAdding(true)
		setError(null)
		try {
			await onAdd(name.trim(), qty, unitId)
			setName('')
			setQty(1)
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to add ingredient')
		} finally {
			setAdding(false)
		}
	}

	return (
		<section>
			<h2 className="mb-4 text-lg font-semibold">Ingredients</h2>

			{/* Existing ingredients */}
			{ingredients.length > 0 && (
				<div className="mb-4 rounded-xl border border-border bg-surface">
					<ul className="divide-y divide-border">
						{ingredients.map((ri) => (
							<li key={ri.id} className="flex items-center justify-between px-4 py-2.5 text-sm">
								<span className="font-medium">{ri.ingredient.name}</span>
								<span className="flex items-center gap-3 text-muted">
									{ri.quantity} {ri.unit.symbol}
									<button
										onClick={() => onDelete(ri)}
										className="ml-1 text-muted hover:text-primary transition-colors"
										aria-label="Remove ingredient"
									>
										&times;
									</button>
								</span>
							</li>
						))}
					</ul>
				</div>
			)}

			{/* Add ingredient row */}
			<div className="flex flex-wrap gap-2">
				<input
					type="text"
					value={name}
					onChange={(e) => setName(e.target.value)}
					placeholder="Ingredient name"
					className={`min-w-0 flex-1 ${inputClass}`}
					onKeyDown={(e) => e.key === 'Enter' && handleAdd()}
				/>
				<input
					type="number"
					min={0}
					step="0.01"
					value={qty}
					onChange={(e) => setQty(Number(e.target.value))}
					className={`w-20 ${inputClass}`}
				/>
				<select
					value={unitId}
					onChange={(e) => setUnitId(e.target.value)}
					className={inputClass}
				>
					{units.map((u) => (
						<option key={u.id} value={u.id}>{u.symbol} — {u.name}</option>
					))}
				</select>
				<button
					onClick={handleAdd}
					disabled={adding || !name.trim()}
					className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-fg hover:bg-primary-hover disabled:opacity-50 transition-colors"
				>
					{adding ? 'Adding…' : 'Add'}
				</button>
			</div>
			{error && <p className="mt-1 text-xs text-primary">{error}</p>}
		</section>
	)
}
