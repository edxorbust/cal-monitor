import axios from 'axios';

/// CHANGE THIS TO YOUR BACKEND URL

const api = axios.create({
  baseURL: 'https://tu-api-backend.railway.app/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;