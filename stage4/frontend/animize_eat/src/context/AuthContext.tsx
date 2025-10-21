import React, { createContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { API_BASE_URL } from '../config';


interface UserInfo {
	id: string;
  username: string;
  avatarUrl?: string;
}

interface AuthContextType {
  user: UserInfo | null;
  login: (user: UserInfo) => void;
  logout: () => void;
  setUser: (user: UserInfo) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    async function fetchUser() {
      const res = await fetch(`${API_BASE_URL}/accounts/me/`, // TODO: create this endpoint that receives valid tokens and returns user id and username
        { credentials: 'include' });
      if (res.ok) {
        const user = await res.json();
        login(user);
      } else {
        logout();
      }
    }
    fetchUser();
  }, []); // empty dependencies list means the effect will eecute itself once when the component is mounted (page reload)

  const login = (userInfo: UserInfo) => {
    // setIsAuthenticated(true);
    setUser(userInfo);
  };

  const logout = () => {
    // setIsAuthenticated(false);
    setUser(null);
    // Optionally: clear cookies or tokens
  };

  return (
    <AuthContext.Provider value={{ 
		// isAuthenticated, 
		user, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
export { AuthContext };
