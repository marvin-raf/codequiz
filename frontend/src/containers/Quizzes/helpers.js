import cookies from "js-cookie";

import {endpoint} from "../../helpers/routeHelpers";

const helpers = {};

// Will only get quiz templates NOT the instances (quizzes instead of
// quizzes_courses)
helpers.getQuizzes = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint(`/quizzes`), {
                method : "GET",
                headers : {"Teacher-Authorization" : cookies.get("teacher")}
            });

            const json = await res.json();

            resolve(json);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
