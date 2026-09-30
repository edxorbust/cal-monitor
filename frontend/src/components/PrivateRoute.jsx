import { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../auth/context';

export default function PrivateRoute({ children }) {
  const { loading, error, retry, logout } = useContext(AuthContext);
  if (!localStorage.getItem('accessToken')) return <Navigate to="/login" replace />;
  if (loading) return <p role="status">Comprobando sesión…</p>;
  if (error) return <div><p role="alert">{error}</p><button onClick={retry}>Reintentar</button><button onClick={logout}>Volver al login</button></div>;
  return children;
}
