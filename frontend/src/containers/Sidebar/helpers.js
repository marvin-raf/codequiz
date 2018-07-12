import cookies from "js-cookie";
const helpers = {};

helpers.signOut = () => {
  return new Promise(async (resolve, reject) => {
    try {
      let cookieHeader;
      let cookieContent;
      let cookieName;
      if (cookies.get("teacher")) {
        cookieHeader = "Teacher-Authorization";
        cookieContent = cookies.get("teacher");
        cookieName = "teacher";
      } else {
        cookieHeader = "Student-Authorization";
        cookieContent = cookies.get("student");
        cookieName = "student";
      }

      const headers = {};

      headers[cookieHeader] = cookieContent;

      const res = await fetch("http://localhost:5000/auth/signout", {
        method: "POST",
        headers
      });

      if (res.status !== 200) {
        reject();
        return;
      }

      cookies.remove(cookieName);
      resolve();
    } catch (e) {
      reject(e);
    }
  });
};

export default helpers;
