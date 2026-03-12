type RecipeFeedErrorProps = {
	message: string
}

export default function RecipeFeedError({ message }: RecipeFeedErrorProps) {
	return (
		<div className="rounded-lg border border-primary/30 bg-primary/5 px-6 py-10 text-center">
			<p className="text-lg font-semibold text-primary">
				Oops, couldn't load recipes
			</p>
			<p className="mt-1 text-sm text-muted">{message}</p>
		</div>
	)
}
