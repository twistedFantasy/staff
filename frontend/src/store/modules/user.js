
import * as authService from "@/services/auth.service";
// initial state
// shape: [{ id, quantity }]
const state = {
  userProfile: {},
  logedUserId: null,
  faq: [],
}

// getters
const getters = {
  getUserProfile: state => state.userProfile
}

// actions
const actions = {

  setUserId ({ commit }) {
    commit('setUserId')
  },
  setUser ({ commit }, userObject) {
    commit('setUser', userObject)
  },
  setFAQ ({ commit }, data) {
    commit('setFAQ', data)
  },
  
  getUser ( { state, dispatch } ) {
    authService
    .getUserById(state.logedUserId)
    .then(data => {
      dispatch('setUser', data);
    })
    .catch(() => {
    });
  },

  onChangeUserProfile ({ state, dispatch }, data) {
    authService.updateUserProfile(state.logedUserId, data).then(
      () => {
        dispatch('getUser');
      },
      () => {}
    );
  },

  getFAQ ({ dispatch }) {
    authService
    .getFAQContent()
    .then(data => {
      dispatch("setFAQ", data.results);
    })
    .catch(() => {});
  }
}

// mutations
const mutations = {
  setUserId (state ) {
    const jwtToken = localStorage.getItem('user');
    if(jwtToken ) {
    var base64Url = jwtToken.split('.')[1];
    var base64 = base64Url.replace('-', '+').replace('_', '/');
    const objectToken = JSON.parse(window.atob(base64));
    const id = objectToken.user_id;
    state.logedUserId = id;
    }
  },
  setUser (state, data ) {
    state.userProfile = data;
  },
  setFAQ (state, data ) {
    state.faq = data;
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}