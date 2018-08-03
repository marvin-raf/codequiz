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
        headers
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

export default helpers;
