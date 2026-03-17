import { Link } from 'react-router-dom'

type UserMenuDropdownProps = {
	onLogout: () => Promise<void>
}

export default function UserMenuDropdown({ onLogout }: UserMenuDropdownProps) {
	return (
		<div className="absolute flex flex-col right-0 mt-2 w-48 rounded-md border border-input bg-surface py-1 shadow-lg z-1">
			{/* TODO: add icons to the dropdown menu items */}
			<Link
				to="/recipes"
				className="w-full px-4 py-2 text-left text-sm text-subtle hover:bg-surface-hover hover:cursor-pointer transition-colors"
			>
				My recipes
			</Link>
			<button
				onClick={async () => {
					await onLogout()
				}}
				className="w-full px-4 py-2 text-left text-sm text-subtle hover:bg-surface-hover hover:cursor-pointer transition-colors"
			>
				Log out
			</button>
		</div>
	)
}
