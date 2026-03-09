import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import avatarIcon from '@/assets/icon.svg'
const POINTER_CHOICE = 'pointer'  // options: pointer or mouse

export default function UserMenu() {
	const { user, logout } = useAuth()
	const [open, setOpen] = useState(false)
	const menuRef = useRef<HTMLDivElement>(null)
	// Close dropdown when clicking outside
	useEffect(() => {
		function handleClickOutside(e: MouseEvent) {
			if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
				setOpen(false)
			}
		}
		document.addEventListener(`${POINTER_CHOICE}down`, handleClickOutside)
		return () => document.removeEventListener(`${POINTER_CHOICE}down`,
			handleClickOutside)
	}, [])
	// show no user menu if the user is not logged-in (no `user` in the
	// AuthContext)
	if (!user) return null

	// TODO: change this to use actual displayName from the profile
	// (once the ProfileUpdatePage will be in service)
	const displayName = user.email

	return (
		// use `position: relative` so that the child dropdown menu can
		// be positioned with respect to it using `position: absolute`
		<div className="relative" ref={menuRef}>
			<button
				// toggle open/closed on click of the button
				onClick={() => setOpen((prev) => !prev)}
				className="flex items-center gap-2 rounded-full p-1 hover:bg-surface-hover hover:cursor-pointer transition-colors"
			>
				<img
					src={user.avatarUrl || avatarIcon}
					alt={`${displayName}'s avatar`}
					className="h-8 w-8 rounded-full object-cover"
				/>
				<span className="text-sm font-medium">{displayName}</span>
			</button>

			{open && (
				// give dropdown `position: absolute` so it is out of
				// the flow of the document (out of the header) and it
				// is positioned with respect to the closest ancestor
				// with non-default (non-static) `position`.
				// As the button is in normal flow, it takes vertical
				// space and, as the dropdown down't declare a `top`
				// property it respects its vertical natural position.
				// `right: 0`, however, sets its right border position
				// to match the right border position of the parent
				// `div` with `relative` positioning. 
				<div className="absolute right-0 mt-2 w-48 rounded-md border border-input bg-surface py-1 shadow-lg z-10">
					{/* TODO: add icons to the dropdown menu items */}
					<button
						onClick={async () => {
							await logout()
							setOpen(false)
						}}
						className="w-full px-4 py-2 text-left text-sm text-subtle hover:bg-surface-hover hover:cursor-pointer transition-colors"
					>
						Log out
					</button>
				</div>
			)}
		</div>
	)
}
