import { useAuth } from "../auth/AuthContext";
import { useNavigate } from "react-router-dom"
import { useState } from "react";

export default function LoginPage() {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [loginValue, setLoginValue] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);

    async function handleSubmit(e) {
        e.preventDefault();
        setError(null);
        try {
            await login(loginValue, password);
            navigate("/", { replace: true });
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>Вход</h1>
            <div>
                <input 
                placeholder="Логин"
                value={loginValue}
                onChange={(e) => setLoginValue(e.target.value)}
                autoComplete="username"
                 />
            </div>
            <div>
                <input 
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                 />
            </div>
            {error && <p>{error}</p>}
            <button type="submit">Войти</button>
        </form>
    );
}