const helpers = {};

helpers.signIn = (email, password) => {
  return new Promise(async (resolve, reject) => {
    const res = await fetch("http://localhost:5000/auth/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email,
        password
      })
    });

    if (res.status !== 200) {
      reject();
      return;
    }

    const json = await res.json();

    resolve(json);
  });
};

export default helpers;
