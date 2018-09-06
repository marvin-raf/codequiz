import cookies from "js-cookie";
import {endpoint} from "../../../helpers/routeHelpers";

const helpers = {};

helpers.addTestCase = (quizId, questionId, testInput, testExpected) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                endpoint(`/quizzes/${quizId}/questions/${questionId}/testcase`),
                {
                    method : "POST",
                    headers : {
                        "Content-Type" : "application/json",
                        "Teacher-Authorization" : cookies.get("teacher"),
                    },
                    body : JSON.stringify({
                        test_input : testInput,
                        test_expected : testExpected,
                    }),
                });

            if (res.status !== 201) {
                reject(res.status);
                return;
            }

            const json = await res.json();

            resolve(json.test_id);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;