import cookies from "js-cookie";
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
        cookieContents = cookies.get("students");
      }

      headers[headerName] = cookieContents;

      const res = await fetch(`http://localhost:5000/quizzes/${quizId}`, {
        headers
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }

      const json = await res.json();

      resolve({
        quizName: json.quiz_name,
        questions: json.questions
      });
    } catch (e) {
      reject(e);
    }
  });
};

export default helpers;
