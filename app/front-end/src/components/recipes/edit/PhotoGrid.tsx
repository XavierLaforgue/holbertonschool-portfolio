import { useRef } from 'react'
import type { RecipePhoto } from '@/types'

interface PhotoGridProps {
	photos: RecipePhoto[]
	uploading: boolean
	error: string | null
	onUpload: (file: File, position: number) => void
	onDelete: (photo: RecipePhoto) => void
}

export default function PhotoGrid({
	photos,
	uploading,
	error,
	onUpload,
	onDelete,
}: PhotoGridProps) {
	const fileInputRef = useRef<HTMLInputElement>(null)

	function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
		if (!e.target.files?.[0]) return
		const file = e.target.files[0]

		// Find first free position (1–5)
		const used = new Set(photos.map((p) => p.position))
		let position = 1
		while (used.has(position) && position <= 5) position++
		if (position > 5) return

		onUpload(file, position)
		if (fileInputRef.current) fileInputRef.current.value = ''
	}

	const sorted = [...photos].sort((a, b) => a.position - b.position)

	return (
		<section>
			<div className="mb-4 flex items-center justify-between">
				<h2 className="text-lg font-semibold">
					Photos <span className="text-sm font-normal text-muted">({photos.length}/5)</span>
				</h2>
				{photos.length < 5 && (
					<>
						<input
							ref={fileInputRef}
							type="file"
							accept="image/jpeg,image/png,image/webp"
							className="hidden"
							onChange={handleFileChange}
						/>
						<button
							onClick={() => fileInputRef.current?.click()}
							disabled={uploading}
							className="rounded-lg border border-border bg-surface px-3 py-1.5 text-sm font-medium hover:bg-surface-hover disabled:opacity-50 transition-colors"
						>
							{uploading ? 'Uploading…' : '+ Upload photo'}
						</button>
					</>
				)}
			</div>

			{error && <p className="mb-2 text-xs text-primary">{error}</p>}

			{photos.length === 0 && (
				<p className="text-sm text-muted">No photos yet. Position 1 will be the main card image.</p>
			)}

			{photos.length > 0 && (
				<div className="grid grid-cols-3 gap-3 sm:grid-cols-5">
					{sorted.map((photo) => (
						<div key={photo.id} className="group relative aspect-square overflow-hidden rounded-lg border border-border">
							<img
								src={photo.image}
								alt={`Position ${photo.position}`}
								className="h-full w-full object-cover"
							/>
							<div className="absolute inset-0 flex flex-col items-center justify-between bg-black/40 p-1 opacity-0 group-hover:opacity-100 transition-opacity">
								<span className="self-start rounded bg-black/60 px-1.5 py-0.5 text-xs text-white">
									{photo.position === 1 ? 'Main' : `#${photo.position}`}
								</span>
								<button
									onClick={() => onDelete(photo)}
									className="rounded-full bg-red-500/80 p-1.5 text-xs text-white hover:bg-red-600 transition-colors"
									aria-label="Delete photo"
								>
									&times;
								</button>
							</div>
						</div>
					))}
				</div>
			)}
		</section>
	)
}
