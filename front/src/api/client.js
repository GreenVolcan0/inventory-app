import { API_URL } from "../config";

let accessToken = null;
let refreshToken = localStorage.getItem("refresh_token");

export function setTokens({ access, refresh }) {
    accessToken = access;
    if (refresh) {
        refreshToken = refresh;
        localStorage.setItem("refresh_token", refresh);
    }
}
export function clearTokens() {
    accessToken = null;
    refreshToken = null;
    localStorage.removeItem("refresh_token");
}

export function getAccessToken() {
    return accessToken;
}

async function refreshAccessToken() {
    if (!refreshToken) throw new Error("no refresh token");
    const res = await fetch(`${API_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!res.ok) {
        clearTokens();
        throw new Error("refresh failed");
    }
    const data = await res.json();
    setTokens({ access: data.access_token, refresh: data.refresh_token });
    return data.access_token;
}

export async function apiFetch(path, options = {}, retry = true) {
    const headers = new Headers(options.headers || {});
    if (accessToken) headers.set("Authorization", `Bearer ${accessToken}`);
    const res = await fetch(`${API_URL}${path}`, { ...options, headers });
    if (res.status === 401 && retry) {
        try {
            await refreshAccessToken();
            return apiFetch(path, options, false);
        } catch {
            clearTokens();
            throw new Error("unauthorized")
        }
    }
    return res;
}
