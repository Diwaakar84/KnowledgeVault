import React, { createContext, useContext, useEffect, useState } from "react";
import { getToken, saveToken, removeToken } from "./authStorage";

interface AuthContextType {
  isLoggedIn: boolean;
  login: (token: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  isLoggedIn: false,
  login: async () => {},
  logout: async () => {},
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function init() {
      const token = await getToken();
      setIsLoggedIn(!!token);
      setLoading(false);
    }

    init();
  }, []);

  async function login(token: string) {
    await saveToken(token);
    setIsLoggedIn(true);
  }

  async function logout() {
    await removeToken();
    setIsLoggedIn(false);
  }

  return (
    <AuthContext.Provider
      value={{ isLoggedIn, login, logout, loading }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
