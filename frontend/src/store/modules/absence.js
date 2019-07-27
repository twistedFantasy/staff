

import * as absenceService from "@/services/absence.service";
// shape: [{ id, quantity }]
const state = {
  allAbsences: [],
  paginationInfo: {
    page: 1,
    limit: 5,
    count: 1,
  },
  filter: {
    reason: "",
    status: "",
    start_date: "",
    end_date: "",
  },
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

  setPaginationInfo ({ commit }, paginationInfo) {
    if(paginationInfo) {
    commit('setPaginationInfo', paginationInfo)
    }
  },

  setFilter ({ commit, dispatch }, data) {
    commit("setFilter", data);
    dispatch("setPaginationInfo", {});
    dispatch("getAbsences");
  },

  getAbsences ({state, dispatch}) {
    const currentpage = state.paginationInfo.page - 1;
    const limit = state.paginationInfo.limit;
    const filters = state.filter;
    const searchParams = new URLSearchParams(filters);
    const filter = `?limit=${limit}&offset=${currentpage *
      limit}&${searchParams.toString()}`;
    absenceService.getAllAbsencesByUserId(filter).then(
      data => {
        dispatch("setAllAbsence", data.results);
        dispatch("setPaginationInfo", { count: Math.ceil(data.count / limit) });
      },
      () => {
      }
    );
  }
}

// mutations
const mutations = {

  setAllAbsence (state, listAbsences ) {
    state.allAbsences = listAbsences;
  },
  setPaginationInfo (state, paginationInfo ) {
    state.paginationInfo = {...state.paginationInfo, ...paginationInfo};
  },
  setFilter (state, data ) {
    if(Object.keys(data).length){
    state.filter = {...state.filter, ...data};
    }
    else {
      state.filter = {};
    }
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}