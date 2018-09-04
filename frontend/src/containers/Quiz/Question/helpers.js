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
                        {"Student-Authorization" : cookies.get("teacher")}
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

helpers.updateQuestion = question => {
    return new Promise(async (resolve, reject) => {
        try {
            console.log("am I over here?");
            const res = await fetch(
                `http://localhost:5000/quizzes/${
                    question.question_quiz_id}/questions/${
                    question.question_id}`,
                {
                    method : "PUT",
                    headers : {
                        "Content-Type" : "application/json",
                        "Teacher-Authorization" : cookies.get("teacher")
                    },
                    body : JSON.stringify({
                        question_description : question.question_description,
                        test_cases : question.test_cases
                    })
                });

            if (res.status !== 200) {
                reject(e);
                return;
            }

            resolve();
        } catch (e) {
            console.log(e);
            reject(e);
        }
    });
};

helpers.addTestCase = (quizId, questionId, testInput, testExpected) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(
                `http://localhost:5000/quizzes/${quizId}/questions/${
                    questionId}/testcase`,
                {
                    method : "POST",
                    headers : {
                        "Content-Type" : "application/json",
                        "Teacher-Authorization" : cookies.get("teacher")
                    },
                    body : JSON.stringify({
                        test_input : testInput,
                        test_expected : testExpected
                    })
                });

            if (res.status !== 201) {
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
