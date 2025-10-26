const getBaseURL = () => {
  const hostname = window.location.hostname;
  
  // Si estamos accediendo localmente
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  // Si es desde red local o internet, usar el mismo host con puerto 8000
  // O mejor aún, usar rutas relativas que pasan por NGINX
  return '';  // Vacío = usa el mismo host y puerto que el frontend
};

export const API_BASE_URL = getBaseURL();

console.log('🔗 API URL:', API_BASE_URL || 'Same origin');

export default {
  baseURL: API_BASE_URL,
  timeout: 60000,
};
