import cookies from "js-cookie";
import { endpoint } from "../../helpers/routeHelpers";

const helpers = {};

helpers.getClass = classId => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(endpoint(`/classes/${classId}`), {
        method: "GET",
        headers: { "Teacher-Authorization": cookies.get("teacher") },
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }

      const json = await res.json();
      const { class_id, class_name } = json.class;
      resolve({ classId: class_id, className: class_name });
    } catch (e) {
      reject(e);
    }
  });
};

helpers.getStudents = classId => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(endpoint(`/classes/${classId}/students`), {
        method: "GET",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
        },
      });

      if (res.status !== 200) {
        reject(res.status);
        return;
      }
      const json = await res.json();

      resolve(json.students);
    } catch (e) {
      reject(e);
    }
  });
};

helpers.checkEmailExists = (classId, email) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(endpoint(`/classes/${classId}/email?email=${email}`), {
        method: "GET",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
        },
      });

      if (res.status === 200) {
        resolve(false);
        return;
      } else if (res.status === 409) {
        resolve(true);
        return;
      } else {
        reject(res.status);
      }
    } catch (e) {
      reject(e);
    }
  });
};

helpers.addStudents = (classId, students) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(endpoint(`/classes/${classId}/students`), {
        method: "POST",
        headers: {
          "Teacher-Authorization": cookies.get("teacher"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ students }),
      });

      if (res.status !== 201) {
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

helpers.deleteStudent = (classId, studentId) => {
  return new Promise(async (resolve, reject) => {
    try {
      const res = await fetch(endpoint(`/classes/${classId}/students/${studentId}`), {
        method: "DELETE",
        headers: { "Teacher-Authorization": cookies.get("teacher") },
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

export default helpers;
