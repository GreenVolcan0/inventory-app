import { createContext, useContext, useState, useEffect } from "react";
import { apiFetch, setTokens, clearTokens, getAccessToken } from "../api/client";
import { API_URL } from "../config";

const AuthContext = createContext(null);

export function useAuth() {
    return useContext(AuthContext);
}

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        (async () => {
            try {
                if (!getAccessToken()) {

                }
                const res = await apiFetch("/users/me");
                if (res.ok) {
                    setUser(await res.json());
                }
            } catch {
                setUser(null);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    async function login(login, password) {
        const body = new URLSearchParams();
        body.set("username", login);
        body.set("password", password);

        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body,
        });
        if (!res.ok) throw new Error("Невереный логин или пароль");

        const data = await res.json();
        setTokens({ access: data.access_token, refresh: data.refresh_token });
        const meRes = await apiFetch("/users/me");
        if (!meRes.ok) throw new Error("Не удалось получить профиль");
        setUser(await meRes.json());
    }

    function logout() {
        clearTokens();
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, loading, login, logout}}>
            {children}
        </AuthContext.Provider>
    )
}