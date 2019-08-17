import Vue from "vue";
import Router from "vue-router";
import Absences from '@/views/Absences.vue';
import Profile from '@/views/Profile.vue';
import Projects from '@/views/Projects.vue';
import Home from '@/views/Home.vue';
import Assessments from '@/views/Assessments.vue';
import CurrentAssessment from  '@/views/CurrentAssessment.vue';


Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/Login",
      name: "Login",
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
          path: 'Projects',
          component: Projects,
        },
        {
          path: 'Assessments',
          component: Assessments,
        },
        {
          path: 'Assessment/:id',
          component: CurrentAssessment,
        },
      ],
      component: Home,
    },
  ]
});
