import React, { useState, useEffect } from 'react';
import AuthContext from './AuthContext';
import type { ReactNode } from 'react';
import { API_BASE_URL } from '../config';
import type { UserInfo } from './AuthContext';



const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const login = (userInfo: UserInfo) => {
    console.log('[AuthProvider] Logging in user:', userInfo.username);
    setUser(userInfo);
    setError(null);
  };

  const logout = () => {
    console.log('[AuthProvider] Logging out user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
    setError(null);
  };

  useEffect(() => {
    const fetchUser = async (token: string) => {
      try {
        console.log('[AuthProvider] Fetching user info...');
        const res = await fetch(`${API_BASE_URL}/accounts/me/`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });

        if (res.ok) {
          const userInfo = await res.json();
          console.log('[AuthProvider] User fetched successfully:', userInfo.username);
          login(userInfo);
          return;
        }

        if (res.status === 401) {
          console.log('[AuthProvider] Access token expired, attempting refresh...');
          const refreshToken = localStorage.getItem('refresh_token');

          if (!refreshToken) {
            console.error('[AuthProvider] No refresh token available');
            throw new Error('No refresh token available');
          }

          const refreshRes = await fetch(`${API_BASE_URL}/tokens/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken }),
          });

          if (refreshRes.ok) {
            const data = await refreshRes.json();
            localStorage.setItem('access_token', data.access);
            console.log('[AuthProvider] Token refreshed successfully');

            // Retry fetching user with new token
            const retryRes = await fetch(`${API_BASE_URL}/accounts/me/`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${data.access}`,
              }
            });

            if (retryRes.ok) {
              const userInfo = await retryRes.json();
              console.log('[AuthProvider] User fetched successfully after refresh:', userInfo.username);
              login(userInfo);
              return;
            } else {
              console.error('[AuthProvider] Failed to fetch user after token refresh');
              throw new Error('Failed to fetch user after token refresh');
            }
          } else {
            console.error('[AuthProvider] Token refresh failed');
            throw new Error('Token refresh failed');
          }
        } else {
          console.error('[AuthProvider] Unexpected response status:', res.status);
          throw new Error(`Unexpected response: ${res.status}`);
        }
      } catch (err) {
        console.error('[AuthProvider] Error in fetchUser:', err);
        throw err;
      }
    };

    const initAuth = async () => {
      const accessToken = localStorage.getItem('access_token');

      // No token = not logged in, finish loading
      if (!accessToken) {
        setIsLoading(false);
        return;
      }

      try {
        await fetchUser(accessToken);
      } catch (err) {
        console.error('[AuthProvider] Failed to initialize auth:', err);
        setError(err instanceof Error ? err.message : 'Authentication initialization failed');
        logout();
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []); // Run once on mount

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      setUser,
      isLoading,
      error
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
