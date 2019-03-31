
import { API_URL } from '../.env';

export const getAllAbsencesByUserId = (dataFilter) => {
  const requestOptions = {
    method: 'GET',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') },
  };
  const url = dataFilter && dataFilter.type && dataFilter.value ? `${API_URL}/api/v1/absences/?${dataFilter.type}=${dataFilter.value}&` : `${API_URL}/api/v1/absences/`;
  return fetch(url, requestOptions)
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

export const editAbsence = (data, id) => {
  const requestOptions = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') },
    body: JSON.stringify(data)
  };
  return fetch(`${API_URL}/api/v1/absences/${id}/`, requestOptions)
  .then(handleResponse)
  .then(user => {
    return user;
  });
}

export const deleteAbsence = (id) => {
  const requestOptions = {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', 'Authorization':  'JWT' + ' ' + localStorage.getItem('user') }
  };
  return fetch(`${API_URL}/api/v1/absences/${id}/`, requestOptions)
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