import React, { useState, useEffect } from 'react';
import AuthContext from './AuthContext';
import type { ReactNode } from 'react';
import { API_BASE_URL } from '../config';
import type { UserInfo } from './AuthContext';



const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) return;
    async function fetchUser(token: string) {
      const res = await fetch(`${API_BASE_URL}/accounts/me/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
        }
      });
      if (res.ok) {
        const userInfo = await res.json();
        login(userInfo);
        return;
      } else if (res.status === 401) {
        const refreshToken = localStorage.getItem('refresh_token');
        const refreshRes = await fetch(`${API_BASE_URL}/tokens/refresh/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh: refreshToken }),
        });
        if (refreshRes.ok) {
          const data = await refreshRes.json();
          localStorage.setItem('access_token', data.access);
          token = data.access;
          const res = await fetch(`${API_BASE_URL}/accounts/me/`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          });
          if (res.ok) {
            const userInfo = await res.json();
            login(userInfo);
            return;
          } else {
            logout();
          }
        } else {
          logout();
        }
      } else {
        logout();
      }
    }
    fetchUser(accessToken);
  }, []); // empty dependencies list means the effect will execute itself once when the component is mounted (page reload)

  const login = (userInfo: UserInfo) => {
    setUser(userInfo);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ 
		user, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
