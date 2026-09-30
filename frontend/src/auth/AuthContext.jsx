import { useState, useEffect, useCallback } from 'react';
import api from '../api/api';
import { errorMessage } from '../api/tracker';
import { useNavigate } from 'react-router-dom';

import { AuthContext } from './context';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const logout = useCallback(() => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setUser(null);
    navigate('/login');
  }, [navigate]);
  const fetchUser = useCallback(async () => {
    if (!localStorage.getItem('accessToken')) {setLoading(false);return;}
    setLoading(true);setError('');
    try { const {data}=await api.get('/auth/me/');setUser(data); }
    catch(err) {setError(errorMessage(err));}
    finally {setLoading(false);}
  }, []);
  const login = async (username, password) => {
    const { data } = await api.post('/auth/token/', { username, password });
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    await fetchUser();
    navigate('/dashboard');
  };
  useEffect(() => {fetchUser();}, [fetchUser]);
  return <AuthContext.Provider value={{ user, login, logout, loading, error, retry: fetchUser }}>{children}</AuthContext.Provider>;
};
