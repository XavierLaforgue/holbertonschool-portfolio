import React, { createContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface UserInfo {
  username: string;
  avatarUrl?: string;
}

interface AuthContextType {
//   isAuthenticated: boolean;
  user: UserInfo | null;
  login: (user: UserInfo) => void;
  logout: () => void;
  setUser: (user: UserInfo) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<UserInfo | null>(null);

  // Example: check for authentication cookies or fetch user info on mount
  useEffect(() => {
    // TODO: Implement logic to check if user is logged in (e.g., check cookies or make API call)
    // If logged in, setIsAuthenticated(true) and setUser(userInfo)
  }, []);

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
