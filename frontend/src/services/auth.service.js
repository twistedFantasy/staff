import axios from 'axios'
const http = require('./http.init');


import { API_URL } from '../.env';

/*
export const makeLogin = ({email, password}) => {
  const id = http.post(`${API_URL}/api/v1/token/obtain/`, {email, password});
  console.log(id, 'id');
  return id;
}
*/

export const getUserById = (id) => {
  const requestOptions = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') },
  };
  return fetch(`${API_URL}/api/v1/users/${id}`, requestOptions)
    .then(handleResponse)
    .then(user => {
      return user;
    });

}

export const makeLogin = (email, password) => {
  const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
  };

  return fetch(`${API_URL}/api/v1/token/obtain/`, requestOptions)
    .then(handleResponse)
    .then(user => {
      if (user.token) {
          localStorage.setItem('user',  user.token);
      }
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