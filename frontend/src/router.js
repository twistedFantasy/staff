import Vue from "vue";
import Router from "vue-router";
import Absences from '@/views/Absences.vue';
import Profile from '@/views/Profile.vue';
import Skills from '@/views/Skills.vue';
Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/Login",
      name: "Login",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Login.vue")
    },
    {
      path: "/Home",
      name: "Home",
      children: [
        {
          path: 'Absences',
          component: Absences,
        },
        {
          path: 'Profile',
          component: Profile,
        },
        {
          path: 'Skills',
          component: Skills,
        },
      ],
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/Home.vue")
    },
  ]
});
