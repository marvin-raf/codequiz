import cookies from "js-cookie";
import {endpoint} from "../../../helpers/routeHelpers";
import studentStore from "../../../store/studentStore";

const helpers = {};

/*
  Precheck prechecks code and returns response from server
*/
helpers.precheck = (quizId, questionId, code) => {
    return new Promise(async (resolve, reject) => {
        try {
            const headers = {"Content-Type" : "application/json"};

            if (studentStore.methods.studentLoggedIn()) {
                headers["Student-Authorization"] = cookies.get("student");
            }

            const res = await fetch(
                endpoint(`/quizzes/${quizId}/questions/${questionId}/precheck`),
                {method : "POST", headers, body : JSON.stringify({code})});

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            const json = await res.json();

            resolve(json.output);
        } catch (e) {
            reject(e);
        }
    });
};

/*
    Check checks code against test cases and returns response
*/
helpers.check = (quizId, questionId, code) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                endpoint(`/quizzes/${quizId}/questions/${questionId}/check`), {
                    method : "POST",
                    headers : {
                        "Content-Type" : "application/json",
                        "Student-Authorization" : cookies.get("student"),
                    },
                    body : JSON.stringify({code}),
                });

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            const json = await res.json();

            resolve(json);
        } catch (e) {
            reject(e);
        }
    });
};

/*
  updateQuestion updates a questions description
*/
helpers.updateQuestion = question => {
    return new Promise(async (resolve, reject) => {
        console.log("Did I make it here");
        try {
            console.log("am I over here?");
            const res = await fetch(
                endpoint(`/quizzes/${question.question_quiz_id}/questions/${
                    question.question_id}`),
                {
                    method : "PUT",
                    headers : {
                        "Content-Type" : "application/json",
                        "Teacher-Authorization" : cookies.get("teacher"),
                    },
                    body : JSON.stringify({
                        question_description : question.question_description,
                    }),
                });

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            resolve();
        } catch (e) {
            console.log(e);
            reject(e);
        }
    });
};

/*
  addQuestion creates a new question in a quiz and returns the question_id
*/
helpers.addQuestion = (description, quizId) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint(`/quizzes/${quizId}/questions`), {
                method : "POST",
                headers : {
                    "Teacher-Authorization" : cookies.get("teacher"),
                    "Content-Type" : "application/json",
                },
                body : JSON.stringify({
                    description,
                }),
            });

            if (res.status !== 201) {
                reject(res.status);
                return;
            }

            const json = await res.json();

            resolve(json.question_id);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
