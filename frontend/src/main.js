import Vue from 'vue'
import App from './App.vue'
import { createStore } from './store'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'
import router from './router'
//import store from "./store";

Vue.use(Vuetify)
Vue.config.productionTip = false
const store = createStore();

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')
