import cookies from "js-cookie";
const helpers = {};

helpers.getCourse = courseId => {
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
      const res = await fetch(`http://localhost:5000/courses/` + courseId, {
        headers,
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }

      const json = await res.json();
      console.log(json);
      resolve({ course: json });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.getClasses = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/classes`, {
        method: "GET",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
      });

      if (res.status != 200) {
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

helpers.addClass = (className, courseId) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/courses` + courseId + `quizzes`, {
        method: "POST",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: courseName,
          start_date: 1543548472,
          end_date: 1553548472,
        }),
      });

      if (res.status !== 201) {
        reject(res.status);
        return;
      }
      const json = await res.json();
      resolve({
        quiz_id: json.quiz_id,
      });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.changeName = (id, name) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/quizzes/` + id, {
        method: "PATCH",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
        }),
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }
      const json = await res.json();
      resolve({});
    } catch (e) {
      reject(e);
    }
  });
};

helpers.changeClass = (id, name) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/classes/` + id, {
        method: "PATCH",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
        }),
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }
      const json = await res.json();
      resolve({});
    } catch (e) {
      reject(e);
    }
  });
};

helpers.getLanguages = () => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/quizzes/languages`, {
        method: "GET",
      });
      const json = await res.json();
      resolve(json);
    } catch (e) {
      reject(e);
    }
  });
};

helpers.createQuiz = (id, name, start_date, end_date, language, description) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/courses/` + id + `/quizzes`, {
        method: "POST",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          start_date: start_date,
          end_date: end_date,
          language: language,
          description: description,
        }),
      });
      if (res.status !== 201) {
        reject(res.status);
        return;
      }
      const json = await res.json();
      resolve({ quiz_id: json.quiz_id });
    } catch (e) {
      reject(e);
    }
  });
};

// Returns both the date and time from a timestamp
// Returns both the date and time from a timestamp
helpers.getDateTime = timestamp => {
  const date = new Date(timestamp);

  const year = date.getFullYear();
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();

  const fullDate = `${year}-${month < 10 ? `0${month}` : month}-${day < 10 ? `0${day}` : day}`;
  const time = `${hours < 10 ? `0${hours}` : hours}:${minutes < 10 ? `0${minutes}` : minutes}`;

  return { date: fullDate, time };
};

export default helpers;
