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
        quizName: json.quiz.quiz_name,
        questions: json.questions,
        quizStartDate: json.quiz.quiz_start_date,
        quizEndDate: json.quiz.quiz_end_date
      });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.addQuestion = (question, quizId) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(
        `http://localhost:5000/quizzes/${quizId}/questions`,
        {
          method: "POST",
          headers: {
            "Teacher-Authorization": cookies.get("teacher"),
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            description: question.question_description,
            test_cases: question.test_cases
          })
        }
      );

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

// Returns both the date and time from a timestamp
helpers.getDateTime = timestamp => {
  const date = new Date(timestamp);

  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();

  const fullDate = `${year}-${month < 10 ? `0${month}` : month}-${
    day < 10 ? `0${day}` : day
  }`;
  const time = `${hours < 10 ? `0${hours}` : hours}:${
    minutes < 10 ? `0${minutes}` : minutes
  }`;

  return { date: fullDate, time };
};

export default helpers;
