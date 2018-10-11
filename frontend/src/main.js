import "bootstrap/dist/css/bootstrap-grid.min.css";
import "vuetify/dist/vuetify.min.css"; // Ensure you are using css-loader

import {library} from "@fortawesome/fontawesome-svg-core";
import {faPython} from "@fortawesome/free-brands-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import Vue from "vue";
import VueRouter from "vue-router";
import Vuetify from "vuetify";

library.add(faPython);

import CodeMirror from "vue-codemirror";
import "codemirror/lib/codemirror.css";

import "codemirror/mode/python/python";
import "codemirror/theme/idea.css";

Vue.use(CodeMirror);

Vue.component("font-awesome-icon", FontAwesomeIcon);

import About from "./containers/About/About.vue";
import App from "./containers/App.vue";
import Class from "./containers/Class/Class.vue";
import Classes from "./containers/Classes/Classes.vue";
import Course from "./containers/Course/Course.vue";
import Courses from "./containers/Courses/Courses.vue";
import Dashboard from "./containers/Dashboard/Dashboard.vue";
import Quizzes from "./containers/Quizzes/Quizzes.vue";
import FreeQuizzes from "./containers/FreeQuizzes/FreeQuizzes.vue";
import Home from "./containers/Home/Home.vue";
import Quiz from "./containers/Quiz/Quiz.vue";

import Signin from "./containers/Signin/Signin.vue";
import Signup from "./containers/Signup/Signup.vue";
import authHelper from "./helpers/authHelper";

Vue.use(Vuetify, {theme : {primary : "#34495e", secondary : "#2ecc71"}});
Vue.use(VueRouter);

const routes = [
    {path : "/", component : Home, beforeEnter : authHelper.loggedInOrOut},
    {
        path : "/about",
        component : About,
        beforeEnter : authHelper.loggedInOrOut,
    },
    {path : "/signup", component : Signup, beforeEnter : authHelper.loggedOut},
    {path : "/signin", component : Signin, beforeEnter : authHelper.loggedOut},
    {
        path : "/dashboard",
        component : Dashboard,
        beforeEnter : authHelper.loggedIn,
    },
    {
        path : "/classes",
        component : Classes,
        beforeEnter : authHelper.teacherLoggedIn,
    },
    {
        path : "/classes/:id",
        component : Class,
        beforeEnter : authHelper.teacherLoggedIn,
    },
    {path : "/courses", component : Courses, beforeEnter : authHelper.loggedIn},
    {
        path : "/courses/:id",
        component : Course,
        beforeEnter : authHelper.loggedIn,
    },
    {
        path : "/quizzes/instance/:id",
        component : Quiz,
        beforeEnter : authHelper.loggedInOrOut,
        props : {isInstance : true},
    },
    {
        path : "/quizzes/template/:id",
        component : Quiz,
        beforeEnter : authHelper.teacherLoggedIn,
        props : {isInstance : false},
    },
    {
        path : "/quizzes",
        component : Quizzes,
        beforeEnter : authHelper.teacherLoggedIn,
    },
    {
        path : "/freequizzes",
        component : FreeQuizzes,
        beforeEnter : authHelper.loggedInOrOut,
    },
];

const router = new VueRouter({routes, mode : "history"});

new Vue({el : "#app", router, render : h => h(App)});
