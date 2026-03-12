type RefreshButtonProps = {
	loadRecipes: () => void,
	isLoading: boolean,
}

export default function RefreshButton({
	loadRecipes,
	isLoading,
}: RefreshButtonProps) {
	return (
		<button
			onClick={loadRecipes}
			disabled={isLoading}
			className="flex items-center gap-1.5 rounded-md border border-border bg-surface px-3 py-1.5 text-sm font-medium text-muted transition-colors hover:bg-surface-hover hover:text-foreground disabled:opacity-50 cursor-pointer"
			aria-label="Refresh recipes"
		>
			<svg 
				xmlns="http://www.w3.org/2000/svg"
				// width="18" height="18" 
				viewBox="0 0 24 24"
				fill="none" stroke="currentColor" stroke-width="2"
				stroke-linecap="round" stroke-linejoin="round"
				className={
					`lucide lucide-refresh-cw-icon lucide-refresh-cw
					h-4 w-4  ${isLoading ? 'animate-spin' : ''}`}
			>
				<path 
					d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"
				/>
				<path d="M21 3v5h-5"/>
				<path 
					d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"
				/>
				<path d="M8 16H3v5"/></svg>
			Refresh
		</button>
	)
}
