import cookies from "js-cookie";

import {endpoint} from "../../helpers/routeHelpers";

const helpers = {};

helpers.getClasses = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(endpoint("/classes"), {
                method : "GET",
                headers : {"Teacher-Authorization" : cookies.get("teacher")},
            });

            if (res.status !== 200) {
                reject(e);
                return;
            }

            const json = await res.json();

            resolve(json.classes);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;
