import Vue from "vue";
import App from "./containers/App.vue";

import VueRouter from "vue-router";
import Vuetify from "vuetify";

import Home from "./containers/Home/Home.vue";
import Info from "./containers/Info/Info.vue";
import Signin from "./containers/Signin/Signin.vue";
import Signup from "./containers/Signup/Signup.vue";

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
    component: Home
  },
  {
    path: "/info",
    component: Info
  },
  {
    path: "/signup",
    component: Signup
  },
  {
    path: "/signin",
    component: Signin
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
