import cookies from "js-cookie";

import {endpoint} from "../../../../helpers/routeHelpers";

const helpers = {};

helpers.deleteQuestion = (quizId, questionId) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                endpoint(`/quizzes/${quizId}/questions/${questionId}`), {
                    method : "DELETE",
                    headers :
                        {"Teacher-Authorization" : cookies.get("teacher")},
                });

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            resolve();
        } catch (e) {
            reject(e);
        }
    });
};

helpers.deleteTestCase = (quizId, questionId, testId) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                endpoint(`/quizzes/${quizId}/questions/${questionId}/testcase/${
                    testId}`),
                {
                    method : "DELETE",
                    headers : {
                        "Content-Type" : "application/json",
                        "Teacher-Authorization" : cookies.get("teacher"),
                    },
                    body : JSON.stringify({test_id : testId}),
                });

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            resolve();
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
