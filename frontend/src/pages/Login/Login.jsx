import React, { useState, useContext } from "react";
import { useLocation } from "react-router-dom";
import { AuthContext } from "../../auth/context";
import styles from "./Login.module.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useContext(AuthContext);
  const [busy, setBusy] = useState(false);
  const location = useLocation();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    if (busy) return;
    setBusy(true);
    try {
      await login(username, password);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          (err.response
            ? "No se pudo iniciar sesión."
            : "No se pudo conectar con el backend. Comprueba que esté iniciado."),
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div className={styles.container}>
        <h2>Iniciar Sesión</h2>
        {location.state?.message && (
          <p role="status">{location.state.message}</p>
        )}
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

          <button
            className="formButton primaryFont"
            type="submit"
            disabled={busy}
          >
            {busy ? "Entrando…" : "Entrar"}
          </button>
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
