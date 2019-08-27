

import * as assessmentService from "@/services/assessment.service";
// shape: [{ id, quantity }]
const state = {
  allAssessments: [],
  allCheckpoints: [],
  tasksOfCheckpoint: [],
  currentAssessment: {},
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
  },
   
  setCurrentAssessment ({commit}, currentAssessment) {
    commit('setCurrentAssessment', currentAssessment)
  },

  setAllCheckoints ({ commit }, listOfCheckpoints) {
    commit('setAllCheckoints', listOfCheckpoints)
  },

  getCheckpoints({state, dispatch}, router) {
    // const assesmentId = router.params.id;
    const filter = `?limit=${10}`;
    assessmentService.getAllCheckpoints(filter).then(
      data => {
        dispatch("setAllCheckoints", data.results);
        //dispatch("setPaginationInfo", { count: Math.ceil(data.count / limit) });
      },
      () => {
      }
    );
  },
  getTasksByCheckpoints({state, dispatch}, checkpointId) {
    const filter = `?checkpoint_id=${checkpointId}&limit=${10}`;
    assessmentService.getAllTasks(filter).then(
      data => {
        dispatch("setAllTasks", data.results);
        //dispatch("setPaginationInfo", { count: Math.ceil(data.count / limit) });
      },
      () => {
      }
    );
  },
  setAllTasks({ commit }, listOfTasks) {
    commit('setAllTasks', listOfTasks)
  }
}

// mutations
const mutations = {
  setAllCheckoints (state, listOfCheckpoints ) {
    state.allCheckpoints = listOfCheckpoints;
  },

  setAllAssessments (state, listOfAssessments ) {
    state.allAssessments = listOfAssessments;
  },
  setPaginationInfo (state, paginationInfo ) {
    state.paginationInfo = {...state.paginationInfo, ...paginationInfo};
  },
  setAllTasks (state, tasks ) {
    state.tasksOfCheckpoint = {...state.tasksOfCheckpoint, ...tasks};
  },
  setCurrentAssessment (state, assessment ) {
    state.currentAssessment = {...state.currentAssessment, ...assessment};
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}