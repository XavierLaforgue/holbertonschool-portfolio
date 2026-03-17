import { useCallback, useEffect, useState } from 'react'
import { apiFetch } from '@/lib/api'

type UseRecipesOptions<T> = {
	autoLoad?: boolean
	initialData: T
}

export function useRecipes<T>(
	endpoint: string,
	options: UseRecipesOptions<T>,
) {
	const { autoLoad = true, initialData } = options
	const [data, setData] = useState<T>(initialData)
	const [isLoading, setIsLoading] = useState(true)
	const [error, setError] = useState<string | null>(null)

	const loadRecipes = useCallback(async () => {
		setIsLoading(true)
		setError(null)
		try {
			const response = await apiFetch<T>(endpoint)
			setData(response)
		} catch (err) {
			setError(err instanceof Error ? err.message : 'Failed to load recipes')
		} finally {
			setIsLoading(false)
		}
	}, [endpoint])

	useEffect(() => {
		if (autoLoad) loadRecipes()
	}, [autoLoad, loadRecipes])

	return {
		data,
		isLoading,
		error,
		loadRecipes,
	}
}
