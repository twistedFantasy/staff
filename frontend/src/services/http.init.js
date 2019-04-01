/**
 * HTTP request layer
 * if auth is required return patched axios instance(with access token in headers)
 * else return clear axios instance
 */

import axios from 'axios'

import * as authService from '../services/auth.service'
import { API_URL } from '../.env'
/*
export default class Http {
  constructor (status) {
    this.isAuth = status && status.auth ? status.auth : false
    this.instance = axios.create({
      baseURL: API_URL
    })

    return this.init()
  }

  init () {
    if (this.isAuth) {
      this.instance.interceptors.request.use(request => {
        request.headers['token'] = authService.getAccessToken()
        // if access token expired and refreshToken is exist >> go to API and get new access token
        if (authService.isAccessTokenExpired() && authService.getRefreshToken()) {
          return authService.refreshTokens()
            .then(response => {
              request.headers['token'] = response.data.accessToken
              return request
            }).catch(error => Promise.reject(error))
        } else {
          return request
        }
      }, error => {
        return Promise.reject(error)
      })

      return this.instance
    }
    return this.instance
  }
}
*/
function getHeaders() {
  return {
    'Authorization': localStorage.getItem('customer_token'),
    'content-type': 'application/json',
  };
}
let _invalidTokenHandler = null;
export function onInvalidToken(foo) {
  _invalidTokenHandler = foo;
}

function request(url, data, method) {
  return axios({
    method,
    url,
    data,
    headers: getHeaders(),
  });
}

axios.interceptors.response.use(
  (response) => response.data,
  (error) => {
    return Promise.reject(error.response.data);
  }
);

export const get = (url) => {
  return request(url, null, 'GET');
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

export const put = (url, data) => {
  return request(url, data, 'PUT');
}