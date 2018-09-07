import emailValidator from "email-validator";
import {endpoint} from "../../helpers/routeHelpers";

const helpers = {};

/*
  Will check for errors and implicitly mutate the errors object
  so errors get reflected in the vue. Returns true if an error
  is found
*/
helpers.formHasErrors = data => {
    if (!data.name) {
        data.errors.name.push("Required Field");
    }

    if (!data.email) {
        data.errors.email.push("Required Field");
    } else if (!emailValidator.validate(data.email)) {
        data.errors.email.push("Invalid Email");
    }

    if (!data.password) {
        data.errors.password.push("Required Field");
    }

    if (!data.confirmPassword) {
        data.errors.confirmPassword.push("Required Field");
    }

    if (data.password && data.confirmPassword &&
        data.password !== data.confirmPassword) {
        data.errors.password.push("Passwords do not match");
        data.errors.confirmPassword.push("Passwords do not match");
    }

    // Check if there were any errors
    for (const key of Object.keys(data.errors)) {
        if (data.errors[key].length)
            return true;
    }
};

// Signs up a new teacher
helpers.signUp = data => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint("/teachers/signup"), {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({
                    name : data.name,
                    email : data.email,
                    password : data.password,
                }),
            });

            if (res.status !== 201) {
                if (res.status === 400) {
                    data.errors.email.push("Email Address already taken");
                }
                reject();
                return;
            }

            resolve();
        } catch (e) {
            reject(e);
        }
    });
};

// Signs in a new teacher
helpers.signIn = data => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint("/auth/signin"), {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify(
                    {email : data.email, password : data.password}),
            });

            if (res.status !== 200) {
                reject();
                return;
            }

            const json = await res.json();
            resolve(json.token);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
