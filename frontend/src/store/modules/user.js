

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

  setUserId ({ state, commit }, id) {
    if(id) {
    commit('setUserId', id)
    }
  },
  setUser ({ state, commit }, userObject) {
    commit('setUser', userObject)
  }
}

// mutations
const mutations = {

  setUserId (state, id ) {
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