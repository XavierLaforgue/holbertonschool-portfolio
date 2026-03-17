interface StatusActionsProps {
	isAuthor: boolean
	statusValue: string
	statusLoading: boolean
	statusError: string | null
	onStatusChange: (newValue: string) => void
	onEdit: () => void
	saveState: 'idle' | 'saving' | 'saved' | 'error'
	onSaveCopy: () => void
}

export default function StatusActions({
	isAuthor,
	statusValue,
	statusLoading,
	statusError,
	onStatusChange,
	onEdit,
	saveState,
	onSaveCopy,
}: StatusActionsProps) {
	return (
		<>
			<div className="mt-4 flex flex-wrap items-center gap-3">
				{isAuthor && (
					<>
						{statusValue !== 'Published' && (
							<button
								onClick={onEdit}
								className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium transition-colors hover:bg-surface-hover hover:cursor-pointer"
							>
								Edit
							</button>
						)}

						{statusValue === 'Draft' && (
							<button
								onClick={() => onStatusChange('Ready')}
								disabled={statusLoading}
								className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 transition-colors hover:cursor-pointer"
							>
								{statusLoading ? 'Updating…' : 'Mark as Ready'}
							</button>
						)}

						{statusValue === 'Ready' && (
							<button
								onClick={() => onStatusChange('Published')}
								disabled={statusLoading}
								className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-50 transition-colors hover:cursor-pointer"
							>
								{statusLoading ? 'Publishing…' : 'Publish'}
							</button>
						)}

						{statusValue === 'Published' && (
							<button
								onClick={() => onStatusChange('Ready')}
								disabled={statusLoading}
								className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium text-muted hover:bg-surface-hover hover:cursor-pointer disabled:opacity-50 transition-colors"
							>
								{statusLoading ? 'Retracting…' : 'Retract'}
							</button>
						)}
					</>
				)}

				{!isAuthor && statusValue === 'Published' && (
					<button
						type="button"
						onClick={onSaveCopy}
						disabled={saveState === 'saving' || saveState === 'saved'}
						className="rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium transition-colors hover:cursor-pointer hover:bg-surface-hover disabled:opacity-60"
					>
						{saveState === 'saving' && 'Saving…'}
						{saveState === 'saved' && 'Saved!'}
						{saveState === 'error' && 'Failed — retry?'}
						{saveState === 'idle' && 'Save a Copy'}
					</button>
				)}
			</div>

			{statusError && (
				<p className="mt-2 text-sm text-primary whitespace-pre-line">{statusError}</p>
			)}
		</>
	)
}
