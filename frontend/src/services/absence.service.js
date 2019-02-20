import axios from 'axios'
const http = require('./http.init');


import { API_URL } from '../.env';

export const getAllAbsencesByUserId = () => {
  const requestOptions = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') },
  };
  return fetch(`${API_URL}/api/v1/absences/`, requestOptions)
    .then(handleResponse)
    .then(user => {
      return user;
    });
}

export const createNewAbsence = (data) => {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') },
    body: JSON.stringify(data)
  };
  return fetch(`${API_URL}/api/v1/absences/`, requestOptions)
    .then(handleResponse)
    .then(user => {
      return user;
    });
}

function handleResponse(response) {
  return response.text().then(text => {
      const data = text && JSON.parse(text);
      if (!response.ok) {
          const error = (data && data.msg) || response.statusText;
          return Promise.reject(error);
      }

      return data;
  });
}