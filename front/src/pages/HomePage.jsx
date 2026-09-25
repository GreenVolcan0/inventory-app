import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom"

export default function HomePage() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    function handleLogout() {
        logout();
        navigate("/login", { replace: true })
    }

    return (
        <div>
            <h1>Инвентаризация</h1>
            {user && <p>{user.login}</p>}
            <button onClick={handleLogout}>Выйти</button>
        </div>
    )
}