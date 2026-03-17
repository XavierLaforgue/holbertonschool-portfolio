export default function RecipeFeedLoading() {
	return (
		<div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
			{Array.from({ length: 6 }).map((_, i) => (
				<div
					key={i}
					className="animate-pulse rounded-xl border border-border bg-surface"
				>
					<div className="h-40 rounded-t-xl bg-surface-hover" />
					<div className="space-y-3 p-4">
						<div className="h-5 w-3/4 rounded bg-surface-hover" />
						<div className="h-3 w-1/4 rounded bg-surface-hover" />
						<div className="h-4 w-full rounded bg-surface-hover" />
						<div className="h-4 w-5/6 rounded bg-surface-hover" />
						<div className="flex gap-3 pt-2">
							<div className="h-3 w-14 rounded bg-surface-hover" />
							<div className="h-3 w-16 rounded bg-surface-hover" />
						</div>
					</div>
				</div>
			))}
		</div>
	)
}
