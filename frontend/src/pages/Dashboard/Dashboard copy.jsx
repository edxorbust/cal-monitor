import React, { useEffect, useState } from "react";
import api from "../../api/api";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get("/user/profile/");
        setUser(response.data);
      } catch (err) {
        // Si no puede obtener el perfil, redirige al login
        navigate("/login");
      }
    };

    fetchUser();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    navigate("/login");
  };

  return (
    <div className="container">
      <h2>Dashboard</h2>
      {user ? (
        <>
          <p>Bienvenido, {user.username}!</p>
          <button onClick={handleLogout}>Cerrar sesión</button>
        </>
      ) : (
        <p>Cargando...</p>
      )}
    </div>
  );
}

export default Dashboard;