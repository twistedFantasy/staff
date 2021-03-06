const http = require('./http.init');
import { API_URL } from '../.env';


export const getUserById = (id) => {
  return http.get(`${API_URL}/api/v1/users/${id}/`);
}

export const makeLogin = (email, password) => {
  return http.post(`${API_URL}/api/v1/token/obtain/`, { email, password });
}

export const updateUserProfile = (id, newUserProfile) => {
  return http.patch(`${API_URL}/api/v1/users/${id}/`, newUserProfile)
}

export const getFAQContent = () => {
  return http.get(`${API_URL}/api/v1/faq/`);
}