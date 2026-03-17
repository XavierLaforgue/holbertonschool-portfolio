import type { RecipePhoto } from '@/types'

type RecipeDetailGalleryProps = {
	photos: RecipePhoto[]
	title: string
}

export default function RecipeDetailGallery({
	photos,
	title,
}: RecipeDetailGalleryProps) {
	if (photos.length === 0) return null

	const sortedPhotos = [...photos].sort((a, b) => a.position - b.position)

	return (
		<div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
			{sortedPhotos.map((photo) => (
				<img
					key={photo.id}
					src={photo.image}
					alt={`${title} - photo ${photo.position}`}
					className="h-32 w-full rounded-lg object-cover"
				/>
			))}
		</div>
	)
}
