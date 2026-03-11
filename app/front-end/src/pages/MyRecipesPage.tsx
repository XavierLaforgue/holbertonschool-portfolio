import MyRecipesGroups, {
	type GroupedRecipes,
	type RecipeGroupKey,
	type RecipeGroupConfig,
} from '@/components/recipes/myrecipes/MyRecipesGroups'
import MyRecipesEmpty from '@/components/recipes/myrecipes/MyRecipesEmpty'
import MyRecipesError from '@/components/recipes/myrecipes/MyRecipesError'
import MyRecipesHeader from '@/components/recipes/myrecipes/MyRecipesHeader'
import MyRecipesLoading from '@/components/recipes/myrecipes/MyRecipesLoading'
import { useRecipes } from '@/hooks/useRecipes'
import { useState } from 'react'

const GROUPS: RecipeGroupConfig[] = [
	{ key: 'draft', title: 'Draft', empty: 'No drafts yet.' },
	{ key: 'ready', title: 'Ready', empty: 'No ready recipes yet.' },
	{ key: 'published', title: 'Published', empty: 'No published recipes yet.' },
	{ key: 'saved', title: 'Saved', empty: 'No saved recipes yet.' },
]

export default function MyRecipesPage() {
	const {
		data,
		isLoading,
		error,
		loadRecipes,
	} = useRecipes<GroupedRecipes>('/api/me/recipes/', {
		initialData: {
			draft: [],
			ready: [],
			published: [],
			saved: [],
		},
	})

	const [openGroups, setOpenGroups] = useState<Record<RecipeGroupKey, boolean>>({
		draft: true,
		ready: true,
		published: true,
		saved: true,
	})

	const hasAnyRecipes = GROUPS.some((group) => data[group.key].length > 0)

	function toggleGroup(key: RecipeGroupKey) {
		setOpenGroups((prev) => ({ ...prev, [key]: !prev[key] })) // later 
		// properties overwrite earlier ones.
	}

	return (
		<section className="container mx-auto px-4 py-12 md:py-16">
			<MyRecipesHeader
				isLoading={isLoading}
				onRefresh={loadRecipes}
			/>

			{error && <MyRecipesError message={error} />}

			{isLoading && !error && <MyRecipesLoading groups={GROUPS} />}

			{!isLoading && !error && !hasAnyRecipes && <MyRecipesEmpty />}

			{!isLoading && !error && (
				<MyRecipesGroups
					groups={GROUPS}
					data={data}
					openGroups={openGroups}
					onToggle={toggleGroup}
				/>
			)}
		</section>
	)
}
