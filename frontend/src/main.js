import Vue from "vue";
import App from "./containers/App.vue";

import VueRouter from "vue-router";
import Vuetify from "vuetify";
import "ace-builds/src-min-noconflict/ace.js";

import Home from "./containers/Home/Home.vue";
import About from "./containers/About/About.vue";
import Signin from "./containers/Signin/Signin.vue";
import Signup from "./containers/Signup/Signup.vue";
import Dashboard from "./containers/Dashboard/Dashboard.vue";
import Classes from "./containers/Classes/Classes.vue";
import Class from "./containers/Class/Class.vue";
import Courses from "./containers/Courses/Courses.vue";
import Course from "./containers/Course/Course.vue";
import Quiz from "./containers/Quiz/Quiz.vue";
import authHelper from "./helpers/authHelper";

import "bootstrap/dist/css/bootstrap-grid.min.css";
import "vuetify/dist/vuetify.min.css"; // Ensure you are using css-loader

Vue.use(Vuetify, {
  theme: {
    primary: "#34495e",
    secondary: "#2ecc71"
  }
});
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: Home,
    beforeEnter: authHelper.loggedInOrOut
  },
  {
    path: "/about",
    component: About,
    beforeEnter: authHelper.loggedInOrOut
  },
  {
    path: "/signup",
    component: Signup,
    beforeEnter: authHelper.loggedOut
  },
  {
    path: "/signin",
    component: Signin,
    beforeEnter: authHelper.loggedOut
  },
  {
    path: "/dashboard",
    component: Dashboard,
    beforeEnter: authHelper.loggedIn
  },
  {
    path: "/classes",
    component: Classes,
    beforeEnter: authHelper.teacherLoggedIn
  },
  {
    path: "/classes/:id",
    component: Class,
    beforeEnter: authHelper.teacherLoggedIn
  },
  {
    path: "/courses",
    component: Courses,
    beforeEnter: authHelper.loggedIn
  },
  {
    path: "/courses/:id",
    component: Course,
    beforeEnter: authHelper.loggedIn
  },
  {
    path: "/quizzes/:id",
    component: Quiz,
    beforeEnter: authHelper.loggedIn
  }
];

const router = new VueRouter({
  routes,
  mode: "history"
});

new Vue({
  el: "#app",
  router,
  render: h => h(App)
});
