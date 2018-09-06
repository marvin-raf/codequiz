const helpers = {};
import {endpoint} from "../../helpers/routeHelpers";

helpers.signIn = (email, password) => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint("/auth/signin"), {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({email, password})
            });

            if (res.status !== 200) {
                reject();
                return;
            }

            const json = await res.json();

            resolve(json);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
