import axios from 'axios'

const checkExparToken = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('customer_token');
    localStorage.removeItem('user');
    window.location = '/Login';
  }
  return response;
}


const extendHeaders = (headers) => {
  const defaultHeaders = {
    'Authorization': 'JWT' + ' ' + localStorage.getItem('user'),
    'content-type': 'application/json',
  };

  return {
    ...defaultHeaders,
    ...headers,
  };
}

function request(url, data, method, headers) {
  return axios({
    method,
    url,
    data,
    headers: extendHeaders(headers),
  });
}

axios.interceptors.response.use(
  (response) => (response.data),
  (error) => {
    checkExparToken(error.response)
    return Promise.reject(error.response.data);
  }
);


export const get = (url, headers) => {
  return request(url, null, 'GET', headers);
}

export const post = (url, data) => {
  return request(url, data, 'POST');
}

export const patch = (url, data) => {
  return request(url, data, 'PATCH');
}

export const del = (url) => {
  return request(url, null, 'DELETE');
}

export const put = (url, data, headers) => {
  return request(url, data, 'PUT', headers);
}