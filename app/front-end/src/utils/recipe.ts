export const DIFF_COLORS: Record<string, string> = {
	easy: 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300',
	medium: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300',
	hard: 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300',
	expert: 'bg-gray-900 text-gray-100 dark:bg-gray-700 dark:text-gray-100',
}

export function formatTime(mins: number): string {
	if (mins < 60) return `${mins} min`
	const h = Math.floor(mins / 60)
	const m = mins % 60
	return m ? `${h}h ${m}min` : `${h}h`
}
