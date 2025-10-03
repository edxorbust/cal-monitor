import React, { createContext, useState, useEffect } from 'react';
import api from '../api/api';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/token/', { username, password });
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      const userRes = await api.get('/auth/me/');
      setUser(userRes.data.user);
      navigate('/dashboard');
    } catch (error) {
      console.error('Error al login', error);
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setUser(null);
    navigate('/login');
  };

  const fetchUser = async () => {
    try {
      const res = await api.get('/auth/me/');
      setUser(res.data);
    } catch {
      logout();
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) fetchUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};