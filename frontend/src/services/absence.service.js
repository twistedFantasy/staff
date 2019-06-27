
import { API_URL } from '../.env';
const http = require('./http.init');

export const getAllAbsencesByUserId = (dataFilter) => {
  const filter = dataFilter || '';
  return http.get(`${API_URL}/api/v1/absences/${filter}`);
}

export const createNewAbsence = (data) => {
  return http.post(`${API_URL}/api/v1/absences/`, data);
}

export const editAbsence = (data, id) => {
  return http.patch(`${API_URL}/api/v1/absences/${id}/`, data);
}

export const deleteAbsence = (id) => {
  return http.del(`${API_URL}/api/v1/absences/${id}/`);
}
