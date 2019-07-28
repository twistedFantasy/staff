import { API_URL } from '../.env';
const http = require('./http.init');

export const getAllProjectsByUserId = (dataFilter) => {
  const filter = dataFilter || '';
  return http.get(`${API_URL}/api/v1/projects/${filter}`);
}