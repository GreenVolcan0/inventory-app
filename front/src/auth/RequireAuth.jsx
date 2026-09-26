import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

export function RequireAuth({ children }) {
    const { user, loading } = useAuth();

    if (loading) return <div>Загрузка...</div>
    if (!user) return <Navigate to="/login" replace />;

    return children;
}

export function RequireGuest({ children }) {
    const { user, loading } = useAuth();

    if (loading) return <div>Загрузка...</div>
    if (user) return <Navigate to="/" replace />;

    return children;
}