import cookies from "js-cookie";
import studentStore from "../../../store/studentStore";

const helpers = {};

helpers.precheck = (quizId, questionId, code) => {
    return new Promise(async (resolve, reject) => {
        try {
            const headers = {"Content-Type" : "application/json"};

            if (studentStore.methods.studentLoggedIn()) {
                headers["Student-Authorization"] = cookies.get("student");
            }

            const res = await fetch(
                `http://localhost:5000/quizzes/${quizId}/questions/${
                    questionId}/precheck`,
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

helpers.check = (quizId, questionId, code) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                `http://localhost:5000/quizzes/${quizId}/questions/${
                    questionId}/check`,
                {
                    method : "POST",
                    headers : {
                        "Content-Type" : "application/json",
                        "Student-Authorization" : cookies.get("student")
                    },
                    body : JSON.stringify({code})
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

helpers.deleteQuestion = (quizId, questionId) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                `http://localhost:5000/quizzes/${quizId}/questions/${
                    questionId}`,
                {
                    method : "DELETE",
                    headers :
                        {"Student-Authorization" : cookies.get("teacher")},
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

helpers.updateQuestion = (question) => {
    return new Promise((resolve, reject) => {
        try {

        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
