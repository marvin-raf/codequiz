const helpers = {};

helpers.getFreeQuizzes = () => {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch("http://localhost:5000/quizzes/free",
                                    {method : "GET"});

            const json = await res.json();

            resolve(json);
        } catch (e) {
            reject(e);
        }
    });
};

export default helpers;