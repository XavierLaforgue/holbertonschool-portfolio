type UserMenuButtonProps = {
	displayName: string
	avatarSrc: string
	onClick: () => void
}

export default function UserMenuButton({
	displayName,
	avatarSrc,
	onClick,
}: UserMenuButtonProps) {
	return (
		<button
			// toggle open/closed on click of the button
			onClick={onClick}
			className="flex items-center gap-2 rounded-full p-1 hover:bg-surface-hover hover:cursor-pointer transition-colors"
		>
			<img
				src={avatarSrc}
				alt={`${displayName}'s avatar`}
				className="h-8 w-8 rounded-full object-cover"
			/>
			<span className="hidden md:inline text-sm font-medium">{displayName}</span>
		</button>
	)
}
