/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');

 var params = {
    "COUCH_USERNAME": "ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix",
    "IAM_API_KEY": "yXZDE1xPrN2KF7m1kEvhm81GxUYz9Abo98b5--5z0Auk",
    "COUCH_URL": "https://ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix.cloudantnosqldb.appdomain.cloud"
}


//  async function main(params) {
async function main() {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
         let dealerships = await new Promise(async resolve => {
             let data = cloudant.db.use('dealerships');
             let documents = await data.list({include_docs:true});
             let results = []
             if(documents.rows.length > 0){
                for(let i = 0; i <= (documents.rows.length - 1); i++){
                    results.push(documents.rows[i].doc);
                }

                resolve(results);
            } else {
                resolve([]);
            }
         });
         return dealerships
     } catch (error) {
         return { error: error.description };
     }
 
}

main()