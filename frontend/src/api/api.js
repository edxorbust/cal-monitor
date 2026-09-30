import axios from 'axios';

const baseURL = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api').replace(/\/$/, '');
const api = axios.create({ baseURL, headers: { 'Content-Type': 'application/json' } });
const authApi = axios.create({ baseURL });
const publicPaths = ['/auth/token/', '/auth/register/', '/auth/token/refresh/'];
let refreshPromise = null;

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token && !publicPaths.includes(config.url)) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const request = error.config;
    if (error.response?.status !== 401 || !request || request._retry || publicPaths.includes(request.url)) {
      return Promise.reject(error);
    }
    request._retry = true;
    const refresh = localStorage.getItem('refreshToken');
    if (refresh) {
      try {
        if (!refreshPromise) {
          refreshPromise = authApi.post('/auth/token/refresh/', { refresh })
            .then(({ data }) => {
              localStorage.setItem('accessToken', data.access);
              return data.access;
            })
            .finally(() => { refreshPromise = null; });
        }
        const access = await refreshPromise;
        request.headers.Authorization = `Bearer ${access}`;
        return api(request);
      } catch {
        // An expired refresh token requires a new login.
      }
    }
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    window.location.href = '/login';
    return Promise.reject(error);
  },
);

export default api;
