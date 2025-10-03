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

  const handleRegister = async (e) => {
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

        <button className="formButton primaryFont" type="submit">Registrarse</button>
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