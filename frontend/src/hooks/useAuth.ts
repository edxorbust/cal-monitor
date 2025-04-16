import { useState, useEffect } from 'react';
import api from '../api/api';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Llamada para obtener datos del usuario logueado
    api.get('/auth/me')
      .then(response => {
        setUser(response.data);
      })
      .catch(error => {
        console.error('No se pudo obtener el usuario', error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return { user, loading };
};