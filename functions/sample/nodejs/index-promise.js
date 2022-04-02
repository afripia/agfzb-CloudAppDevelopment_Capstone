/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');

var params = {
    "COUCH_USERNAME": "ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix",
    "IAM_API_KEY": "yXZDE1xPrN2KF7m1kEvhm81GxUYz9Abo98b5--5z0Auk",
    "COUCH_URL": "https://ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix.cloudantnosqldb.appdomain.cloud"
}

// function main(params) {
function main(params) {

    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    let dbListPromise = getDbs(cloudant);
    return dbListPromise;
}

function getDbs(cloudant) {
    return new Promise((resolve, reject) => {
        cloudant.db.list()
            .then(body => {
                resolve({ dbs: body });
            })
            .catch(err => {
                reject({ err: err });
            });
    });
}
