import { API_URL } from '../.env';
const http = require('./http.init');

export const getAllAssessmentsByUserId = (dataFilter) => {
  const filter = dataFilter || '';
  return http.get(`${API_URL}/api/v1/assessments/${filter}`);
}

export const getAllCheckpoints = (filter) => {
  return http.get(`${API_URL}/api/v1/checkpoints/${filter}`)
}

export const getAllTasks = (filter) => {
  return http.get(`${API_URL}/api/v1/tasks/${filter}`)
}