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
			onSaveCopy={onSaveCopy}
		/>
	)
}
