import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // CAMBIAR A LA URL DEL BACKEND!!!!
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
    (response) => {
      return response; // Si la respuesta es exitosa, la retornamos directamente
    },
    async (error) => {
      const originalRequest = error.config;
  
      // Si el error es 401 (no autorizado) y no hemos intentado refrescar el token antes
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
  
        // Tratamos de refrescar el token
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
          try {
            // Hacemos la solicitud para refrescar el token
            const response = await axios.post('https://tu-api-backend.railway.app/api/auth/token/refresh/', { refresh: refreshToken });
            
            // Guardamos el nuevo access token
            const newAccessToken = response.data.access;
            localStorage.setItem('accessToken', newAccessToken);
            
            // Volvemos a intentar la solicitud original con el nuevo token
            originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
            return axios(originalRequest); // Hacemos la solicitud original de nuevo con el nuevo token
          } catch (refreshError) {
            // Si el refresh token también falla (por ejemplo, si también expiró), cerramos sesión
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            window.location.href = '/login'; // Redirige a la página de login
          }
        } else {
          // Si no tenemos un refresh token, cerramos sesión
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login'; // Redirige a la página de login
        }
      }
      return Promise.reject(error); // Si la respuesta es otro error, lo rechazamos
    }
  );
  

export default api;