

import * as projectService from "@/services/project.service";
// shape: [{ id, quantity }]
const state = {
  allProjects: [],
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
  setAllProjects ({ commit }, listOfProjects) {
    if(listOfProjects.length) {
    commit('setAllProjects', listOfProjects)
    }
  },

  setPaginationInfo ({ commit }, paginationInfo) {
    if(paginationInfo) {
    commit('setPaginationInfo', paginationInfo)
    }
  },

  getProjects ({state, dispatch}) {
    const currentpage = state.paginationInfo.page - 1;
    const limit = state.paginationInfo.limit;
    const filter = `?limit=${limit}&offset=${currentpage *
      limit}`;
      projectService.getAllProjectsByUserId(filter).then(
      data => {
        dispatch("setAllProjects", data.results);
        dispatch("setPaginationInfo", { count: Math.ceil(data.count / limit) });
      },
      () => {
      }
    );
  }
}

// mutations
const mutations = {

  setAllProjects (state, listOfProjects ) {
    state.allProjects = listOfProjects;
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