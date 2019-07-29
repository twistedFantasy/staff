

import * as assessmentService from "@/services/assessment.service";
// shape: [{ id, quantity }]
const state = {
  allAssessments: [],
  paginationInfo: {
    page: 1,
    limit: 5,
    count: 1,
  },
}

// getters
const getters = {

}

// actions
const actions = {
  setAllAssessments ({ commit }, listOfAssessments) {
    if(listOfAssessments.length) {
    commit('setAllAssessments', listOfAssessments)
    }
  },

  setPaginationInfo ({ commit }, paginationInfo) {
    if(paginationInfo) {
    commit('setPaginationInfo', paginationInfo)
    }
  },

  getAssessments ({state, dispatch}) {
    const currentpage = state.paginationInfo.page - 1;
    const limit = state.paginationInfo.limit;
    const filter = `?limit=${limit}&offset=${currentpage *
      limit}`;
      assessmentService.getAllAssessmentsByUserId(filter).then(
      data => {
        dispatch("setAllAssessments", data.results);
        dispatch("setPaginationInfo", { count: Math.ceil(data.count / limit) });
      },
      () => {
      }
    );
  }
}

// mutations
const mutations = {

  setAllAssessments (state, listOfAssessments ) {
    state.allAssessments = listOfAssessments;
  },
  setPaginationInfo (state, paginationInfo ) {
    state.paginationInfo = {...state.paginationInfo, ...paginationInfo};
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}