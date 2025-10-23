import { createContext } from "react";


export interface UserInfo {
	id: string;
  username: string;
  avatarUrl: string;
}

interface AuthContextType {
  user: UserInfo | null;
  login: (user: UserInfo) => void;
  logout: () => void;
  setUser: (user: UserInfo) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export default AuthContext;
