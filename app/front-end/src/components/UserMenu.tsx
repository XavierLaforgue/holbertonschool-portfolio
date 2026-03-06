import { useState, useRef, useEffect } from 'react'
import { useAuth } from '@/hooks/useAuth'
import avatarIcon from '@/assets/icon.svg'

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
		document.addEventListener('mousedown', handleClickOutside)
		return () => document.removeEventListener('mousedown', handleClickOutside)
	}, [])

	if (!user) return null

	return (
		<div className="relative" ref={menuRef}>
			<button
				onClick={() => setOpen((prev) => !prev)}
				className="flex items-center gap-2 rounded-full p-1 hover:bg-surface-hover hover:cursor-pointer transition-colors"
			>
				<img
					src={user.avatarUrl ?? avatarIcon}
					alt={`${user.name}'s avatar`}
					className="h-8 w-8 rounded-full object-cover"
				/>
				<span className="text-sm font-medium">{user.name}</span>
			</button>

			{open && (
				<div className="absolute right-0 mt-2 w-48 rounded-md border border-input bg-surface py-1 shadow-lg">
					<button
						onClick={() => {
							logout()
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
