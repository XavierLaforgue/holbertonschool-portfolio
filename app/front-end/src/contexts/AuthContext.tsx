import { createContext } from 'react'
import type { AuthContextType } from '@/types'

/**
 * AuthContext — holds the current user + auth helpers.
 *
 * Don't use this directly. Use the `useAuth()` hook instead.
 */
export const AuthContext = createContext<AuthContextType | undefined>(undefined)

