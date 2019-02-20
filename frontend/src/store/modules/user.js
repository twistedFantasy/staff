

// initial state
// shape: [{ id, quantity }]
const state = {
  userProfile: {},
  logedUserId: null,
}

// getters
const getters = {

}

// actions
const actions = {

  setUserId ({ state, commit }) {
    commit('setUserId')
  },
  setUser ({ state, commit }, userObject) {
    commit('setUser', userObject)
  }
}

// mutations
const mutations = {

  setUserId (state ) {
    const jwtToken = localStorage.getItem('user');
    var base64Url = jwtToken.split('.')[1];
    var base64 = base64Url.replace('-', '+').replace('_', '/');
    const objectToken = JSON.parse(window.atob(base64));
    const id = objectToken.user_id;
    state.logedUserId = id;
  },
  setUser (state, data ) {
    state.userProfile = data;
  },

}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}