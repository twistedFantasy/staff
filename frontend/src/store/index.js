import Vue from "vue";
import Vuex from "vuex";

import user from './modules/user';
import absence from './modules/absence';
import project from './modules/project';
Vue.use(Vuex);

export function createStore () {
  return new Vuex.Store({
    modules: {
      user,
      absence,
      project,
    },
  })
}