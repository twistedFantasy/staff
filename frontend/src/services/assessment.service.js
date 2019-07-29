import { API_URL } from '../.env';
const http = require('./http.init');

export const getAllAssessmentsByUserId = (dataFilter) => {
  const filter = dataFilter || '';
  return http.get(`${API_URL}/api/v1/assessments/${filter}`);
}