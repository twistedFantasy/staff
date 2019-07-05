

// initial state
// shape: [{ id, quantity }]
const state = {
  allAbsences: [],
  paginationInfo: {},
  FAQContent: {},
}

// getters
const getters = {

}

// actions
const actions = {

  setAllAbsence ({ state, commit }, listAbsences) {
    if(listAbsences.length) {
    commit('setAllAbsence', listAbsences)
    }
  },
  setFAQ ({ state, commit }, data) {
    commit('setFAQ', data)
  }
}

// mutations
const mutations = {

  setAllAbsence (state, listAbsences ) {
    state.allAbsences = listAbsences;
  },

  setFAQ (state, data ) {
    state.FAQContent = data;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}