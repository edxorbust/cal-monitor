import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import styles from "./Login.module.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/token/", {
        username,
        password,
      });

      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);

      navigate("/dashboard");
    } catch (err) {
      setError("Credenciales inválidas. Intenta nuevamente.");
    }
  };

  return (
    <>
    <div className={styles.container}>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleLogin}>
        <div className={styles.formdiv}>
          <input
          className="inputField"
            placeholder="Usuario"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        

        <div className={styles.formdiv}>
          <input
            placeholder="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className={styles.linksbox}>
          <a href="/forgot-password" className={styles.forgotPasswordLink}>
            Olvidé mi contraseña
          </a>
        </div>

        <button className="formButton primaryFont" type="submit">Entrar</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
      </form>
      <div className={styles.linksboxend}>
          <a href="/register" className={styles.registerLink}>
            ¿No tienes una cuenta? Regístrate
          </a>
      </div>
    </div>
    </>
  );
}

export default Login;