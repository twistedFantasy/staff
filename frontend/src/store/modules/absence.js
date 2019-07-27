

// initial state
// shape: [{ id, quantity }]
const state = {
  allAbsences: [],
  paginationInfo: {},
}

// getters
const getters = {

}

// actions
const actions = {

  setAllAbsence ({ commit }, listAbsences) {
    if(listAbsences.length) {
    commit('setAllAbsence', listAbsences)
    }
  },
}

// mutations
const mutations = {

  setAllAbsence (state, listAbsences ) {
    state.allAbsences = listAbsences;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}