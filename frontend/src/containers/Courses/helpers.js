import cookies from "js-cookie";
const helpers = {};
// Get course names
helpers.getCourses = () => {
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

      const res = await fetch(`http://localhost:5000/courses`, {
        headers
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }

      const json = await res.json();
      resolve({
        courses: json.courses
      });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.addCourse = courseName => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/courses`, {
        method: "POST",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: courseName
        })
      });

      if (res.status !== 201) {
        reject(res.status);
        return;
      }
      const json = await res.json();
      resolve({
        course_id: json.course_id
      });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.changeName = (id, name) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(`http://localhost:5000/courses/` + id, {
        method: "PATCH",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: name
        })
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

export default helpers;
