import StatusActions from '../../../components/recipes/StatusActions'

export type RecipeDetailSaveState = 'idle' | 'saving' | 'saved' | 'error'

type RecipeDetailActionsProps = {
	isAuthor: boolean
	statusValue: string
	statusLoading: boolean
	statusError: string | null
	onStatusChange: (value: string) => void
	onEdit: () => void
	saveState: RecipeDetailSaveState
	saveError: string | null
	onSaveCopy: () => void
}

export default function RecipeDetailActions({
	isAuthor,
	statusValue,
	statusLoading,
	statusError,
	onStatusChange,
	onEdit,
	saveState,
	saveError,
	onSaveCopy,
}: RecipeDetailActionsProps) {
	return (
		<StatusActions
			isAuthor={isAuthor}
			statusValue={statusValue}
			statusLoading={statusLoading}
			statusError={statusError}
			onStatusChange={onStatusChange}
			onEdit={onEdit}
			saveState={saveState}
			saveError={saveError}
			onSaveCopy={onSaveCopy}
		/>
	)
}
