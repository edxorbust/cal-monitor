import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/api";
import styles from "./Register.module.css";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const [busy, setBusy] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden.");
      return;
    }
    if (busy) return;
    setBusy(true);
    try {
      await api.post("/auth/register/", {
        username,
        email,
        password,
        password2: confirmPassword,
      });
      navigate("/login", {
        state: { message: "Cuenta creada. Ya puedes iniciar sesión." },
      });
    } catch (err) {
      const details = err.response?.data;
      setError(
        details && typeof details === "object"
          ? Object.values(details).flat().join(" ")
          : "No se pudo conectar con el backend. Comprueba que esté iniciado.",
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div className={styles.container}>
        <h2>Registrarse</h2>
        <form onSubmit={handleRegister}>
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
              className="inputField"
              placeholder="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
          <div className={styles.formdiv}>
            <input
              placeholder="Confirmar Contraseña"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>
          {password !== confirmPassword && (
            <p style={{ color: "red" }}>Las contraseñas no coinciden.</p>
          )}

          <button
            className="formButton primaryFont"
            type="submit"
            disabled={busy}
          >
            {busy ? "Creando cuenta…" : "Registrarse"}
          </button>
          {error && <p style={{ color: "red" }}>{error}</p>}
        </form>
        <div className={styles.linksboxend}>
          <a href="/login" className={styles.registerLink}>
            ¿Ya tienes una cuenta? Inicia sesión
          </a>
        </div>
      </div>
    </>
  );
}

export default Register;
