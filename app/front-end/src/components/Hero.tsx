import Itadakimasu from '@/components/Itadakimasu.tsx'

export default function Hero() {
	return (
		<section className="relative overflow-hidden bg-linear-to-br from-primary/10 via-background to-accent/10 py-16 md:py-24">
			<div className="container mx-auto px-4 text-center">
				<Itadakimasu whichMargin={`mb-4`} repCount={3} />

				<h1 className="text-4xl font-extrabold leading-tight tracking-tight md:text-5xl lg:text-6xl">
					Recipes Straight Out of{' '}
					<span className="bg-linear-to-r from-primary to-accent bg-clip-text text-transparent">
						Your Favorite Anime
					</span>
				</h1>

				<h1 className="text-2xl font-bold leading-tight tracking-tight md:text-3xl lg:text-4xl">
					<span className="bg-linear-to-t from-accent to-primary bg-clip-text text-transparent">
						anime straight{' '}
					</span>
					into your life
				</h1>

				<p className="mx-auto mt-4 max-w-2xl text-lg text-muted md:text-xl">
					Cook the dishes you've always dreamed about, from Naruto's
					legendary ichiraku ramen to Totoro's bento. 
					Share your creations with the community and let your passion for anime and food come alive.
				</p>
				
				<Itadakimasu whichMargin={`mt-4`} repCount={3} />
			</div>

			{/* Soft decorative blobs */}
			<div className="pointer-events-none absolute -top-20 -left-20 h-72 w-72 rounded-full bg-primary/5 blur-3xl" />
			<div className="pointer-events-none absolute -right-20 -bottom-20 h-72 w-72 rounded-full bg-accent/5 blur-3xl" />
		</section>
	)
}
