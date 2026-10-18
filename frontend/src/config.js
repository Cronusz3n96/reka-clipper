const DEV = import.meta.env.DEV;

export const API_BASE_URL = DEV
  ? 'http://localhost:8000'
  : 'https://reka-clipper-api.onrender.com';
