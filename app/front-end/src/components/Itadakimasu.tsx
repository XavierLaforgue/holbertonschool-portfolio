import type { ItadakimasuProps } from '@/types'

export default function Itadakimasu({
	whichMargin = 'mb-4',
	repCount = 3
	}: ItadakimasuProps) {
		return (
			<>
			{Array.from({ length: repCount }).map((_, i) => (
				<span key={i} 
				className={`${whichMargin} inline-block rounded-full bg-primary/10 px-5 py-1 text-sm font-semibold text-primary`}
				>
					Itadakimasu!
				</span>
			))}
			</>
		)
	}
