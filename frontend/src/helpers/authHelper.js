import cookies from "js-cookie";

import {endpoint} from "../helpers/routeHelpers";
import studentStore from "../store/studentStore";
import teacherStore from "../store/teacherStore";

const authHelper = {};

/*
  Checks if a teacher is logged in to go to the next route.
  If they are not logged in, then redirect to signin page
*/
authHelper.teacherLoggedIn = async (to, from, next) => {
    if (!cookies.get("teacher")) {
        next("/signin");
        return;
    }
    try {
        const res = await fetch(endpoint("/teachers/me"), {
            method : "GET",
            headers : {"Teacher-Authorization" : cookies.get("teacher")},
        });

        if (res.status !== 200) {
            next("/signin");
            return;
        }

        const json = await res.json();

        teacherStore.methods.setData(json);

        next();
    } catch (e) {
        next("/signin");
    }
};

/*
  Checks if a student is logged in to go to the next route.
  If they are not logged in, then redirect to signin page
*/
authHelper.studentLoggedIn = async (to, from, next) => {
    if (!cookies.get("student")) {
        next("/signin");
        return;
    }
    try {
        const res = await fetch(endpoint("/students/me"), {
            method : "GET",
            headers : {"Student-Authorization" : cookies.get("student")},
        });

        if (res.status !== 200) {
            next("/signin");
            return;
        }

        const json = await res.json();

        studentStore.methods.setData(json);
        next();
    } catch (e) {
        next("/signin");
    }
};

/*
  Checks if a teacher or student is logged in to go to the next route.
  If they are not logged in, then redirect to signin page
*/

authHelper.loggedIn = async (to, from, next) => {
    let token;
    let isTeacher;
    if (cookies.get("teacher")) {
        token = cookies.get("teacher");
        isTeacher = true;
    } else if (cookies.get("student")) {
        token = cookies.get("student");
        isTeacher = false;
    } else {
        next("/signin");
        return;
    }

    try {
        const headers = {};

        headers[isTeacher ? "Teacher-Authorization" : "Student-Authorization"] =
            token;

        const res = await fetch(isTeacher ? endpoint("/teachers/me")
                                          : endpoint("/students/me"),
                                {method : "GET", headers});

        if (res.status !== 200) {
            next("/signin");
            return;
        }

        const json = await res.json();

        if (isTeacher) {
            teacherStore.methods.setData(json);
        } else {
            studentStore.methods.setData(json);
        }

        next();
    } catch (e) {
        next("/signin");
    }
};

authHelper.loggedInOrOut = async (to, from, next) => {
    let token;
    let isTeacher;
    if (cookies.get("teacher")) {
        token = cookies.get("teacher");
        isTeacher = true;
    } else if (cookies.get("student")) {
        token = cookies.get("student");
        isTeacher = false;
    } else {
        next();
        return;
    }

    try {
        const headers = {};

        headers[isTeacher ? "Teacher-Authorization" : "Student-Authorization"] =
            token;

        const res = await fetch(isTeacher ? endpoint("/teachers/me")
                                          : endpoint("/students/me"),
                                {method : "GET", headers});

        if (res.status !== 200) {
            next();
            return;
        }

        const json = await res.json();

        if (isTeacher) {
            teacherStore.methods.setData(json);
        } else {
            studentStore.methods.setData(json);
        }

        next();
    } catch (e) {
        next();
    }
};

export default authHelper;
