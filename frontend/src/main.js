import Vue from "vue";
import App from "./containers/App.vue";

import VueRouter from "vue-router";
import Vuetify from "vuetify";

import Home from "./containers/Home/Home.vue";
import Info from "./containers/Info/Info.vue";

import authHelper from "./helpers/authHelper";

import "vuetify/dist/vuetify.min.css"; // Ensure you are using css-loader

Vue.use(Vuetify);
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: Home
  },
  {
    path: "/info",
    component: Info
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
