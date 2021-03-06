import cookies from "js-cookie";

import {endpoint} from "../../helpers/routeHelpers";

const helpers = {};

helpers.getFreeQuizzes = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const res =
                await fetch(endpoint("/quizzes/free"), {method : "GET"});

            const json = await res.json();

            resolve(json);
        } catch (e) {
            console.log(e);
            reject(e);
        }
    });
};

helpers.getLanguages = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const res =
                await fetch(endpoint("/quizzes/languages"), {method : "GET"});

            const json = await res.json();

            resolve(json);
        } catch (e) {
            reject(e);
        }
    });
};

helpers.createFreeQuiz = (quizName, quizLanguageId, quizShortDesc) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint("/quizzes/free"), {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json",
                    "Teacher-Authorization" : cookies.get("teacher"),
                },
                body : JSON.stringify({
                    quiz_name : quizName,
                    quiz_language_id : quizLanguageId,
                    quiz_short_desc : quizShortDesc,
                }),
            });

            if (res.status === 201) {
                resolve();
            } else {
                reject(res.status);
            }
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
