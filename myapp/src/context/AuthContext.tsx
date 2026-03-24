import { createContext, useContext, useState, ReactNode } from "react";

export interface AuthUser {
  id: number;
  username: string;
  email: string;
  balance?: number;
  token: string;
}

interface AuthContextType {
  user: AuthUser | null;
  login: (user: AuthUser) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  login: () => {},
  logout: () => {},
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(() => {
    const stored = localStorage.getItem("ts_user");
    return stored ? JSON.parse(stored) : null;
  });

  const login = (u: AuthUser) => {
    setUser(u);
    localStorage.setItem("ts_user", JSON.stringify(u));
    localStorage.setItem("ts_token", u.token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("ts_user");
    localStorage.removeItem("ts_token");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
