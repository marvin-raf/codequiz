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

export default helpers;
