import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * Parse a Django DurationField string ("HH:MM:SS") into total seconds.
 */
function parseDurationToSeconds(duration: string): number {
	const parts = duration.split(':').map(Number)
	if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2]
	if (parts.length === 2) return parts[0] * 60 + parts[1]
	return parts[0] ?? 0
}

/**
 * Format total seconds as "MM:SS" or "H:MM:SS".
 */
function formatSeconds(total: number): string {
	const h = Math.floor(total / 3600)
	const m = Math.floor((total % 3600) / 60)
	const s = total % 60
	const mm = String(m).padStart(2, '0')
	const ss = String(s).padStart(2, '0')
	return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`
}

interface StepTimerProps {
	/** Duration string from the backend, e.g. "00:15:00" */
	duration: string
}

export default function StepTimer({ duration }: StepTimerProps) {
	const initial = parseDurationToSeconds(duration)
	const [remaining, setRemaining] = useState(initial)
	const [isRunning, setIsRunning] = useState(false)
	const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

	const clear = useCallback(() => {
		if (intervalRef.current) {
			clearInterval(intervalRef.current)
			intervalRef.current = null
		}
	}, [])

	useEffect(() => {
		if (!isRunning) {
			clear()
			return
		}
		intervalRef.current = setInterval(() => {
			setRemaining((prev) => {
				if (prev <= 1) {
					setIsRunning(false)
					return 0
				}
				return prev - 1
			})
		}, 1000)
		return clear
	}, [isRunning, clear])

	const done = remaining === 0
	const progress = initial > 0 ? remaining / initial : 0
	const paused = !isRunning && !done && remaining !== initial

	// Pick colors based on state
	const barColor = done ? 'bg-green-500' : isRunning ? 'bg-primary' : 'bg-border'
	const textColor = done ? 'text-green-500' : isRunning ? 'text-foreground' : 'text-muted'

	// Button label changes based on state
	const buttonLabel = 
		isRunning 
		? 'Pause' 
		: done
			? 'Restart'
			: paused
				? 'Resume'
				: 'Start'

	function handleMainButton() {
		if (done) {
			setRemaining(initial)
			setIsRunning(true)
		} else {
			setIsRunning((r) => !r)
		}
	}

	function handleReset() {
		setIsRunning(false)
		setRemaining(initial)
	}

	const showReset = (isRunning || remaining !== initial) && !done

	return (
		<div className="flex flex-col gap-2">
			{/* Time display */}
			<span className={`font-mono text-lg font-semibold tabular-nums ${textColor}`}>
				{formatSeconds(remaining)}
			</span>

			{/* Progress bar */}
			<div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-hover">
				<div
					className={`h-full rounded-full transition-all duration-1000 ease-linear ${barColor}`}
					style={{ width: `${progress * 100}%` }}
				/>
			</div>

			{/* Controls */}
			<div className="flex gap-2">
				<button
					type="button"
					onClick={handleMainButton}
					className="rounded-md border border-border bg-surface px-3 py-1 text-xs font-medium text-muted transition-colors hover:bg-surface-hover hover:text-foreground cursor-pointer"
				>
					{buttonLabel}
				</button>
				{showReset && (
					<button
						type="button"
						onClick={handleReset}
						className="rounded-md border border-border bg-surface px-3 py-1 text-xs font-medium text-muted transition-colors hover:bg-surface-hover hover:text-foreground cursor-pointer"
					>
						Reset
					</button>
				)}
			</div>
		</div>
	)
}
