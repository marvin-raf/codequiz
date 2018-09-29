import cookies from "js-cookie";
import {endpoint} from "../../helpers/routeHelpers";
const helpers = {};

// Get quiz name, id and questions
helpers.getQuizData = quizId => {
    return new Promise(async (resolve, reject) => {
        try {
            let headerName;
            let cookieContents;

            const headers = {};

            if (cookies.get("teacher")) {
                headerName = "Teacher-Authorization";
                cookieContents = cookies.get("teacher");
            } else {
                headerName = "Student-Authorization";
                cookieContents = cookies.get("student");
            }

            headers[headerName] = cookieContents;

            const res = await fetch(endpoint(`/quizzes/${quizId}`), {headers});

            if (res.status !== 200) {
                reject(res.status);
                return;
            }

            const json = await res.json();
            resolve({
                quizName : json.quiz.quiz_name,
                questions : json.questions,
                qcStartDate : json.quiz.quiz_start_date,
                qcEndDate : json.quiz.quiz_end_date,
                qcCourseId : json.quiz.qc_course_id,
                quizTeacherId : json.quiz.teacher_id,
            });
        } catch (e) {
            reject(e);
        }
    });
};

// Returns both the date and time from a timestamp
helpers.getDateTime = timestamp => {
    const date = new Date(timestamp * 1000);

    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hours = date.getHours();
    const minutes = date.getMinutes();

    const fullDate = `${year}-${month < 10 ? `0${month}` : month}-${
        day < 10 ? `0${day}` : day}`;
    const time = `${hours < 10 ? `0${hours}` : hours}:${
        minutes < 10 ? `0${minutes}` : minutes}`;

    return {date : fullDate, time};
};

export default helpers;
