import cookies from "js-cookie";
import {endpoint} from "../../helpers/routeHelpers";
import studentStore from "../../store/studentStore";
import teacherStore from "../../store/teacherStore";

const helpers = {};

helpers.signOut = () => {
    return new Promise(async (resolve, reject) => {
        try {
            let cookieHeader;
            let cookieContent;
            let cookieName;
            if (cookies.get("teacher")) {
                cookieHeader = "Teacher-Authorization";
                cookieContent = cookies.get("teacher");
                cookieName = "teacher";
            } else {
                cookieHeader = "Student-Authorization";
                cookieContent = cookies.get("student");
                cookieName = "student";
            }

            const headers = {};

            headers[cookieHeader] = cookieContent;

            const res = await fetch(endpoint("/auth/signout"),
                                    {method : "POST", headers});

            if (res.status !== 200) {
                reject();
                return;
            }

            if (cookieName === "teacher") {
                teacherStore.methods.signout();
            } else {
                studentStore.methods.signout();
            }

            cookies.remove(cookieName);
            resolve();
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
