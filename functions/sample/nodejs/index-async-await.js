/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');

var params = {
    "COUCH_USERNAME": "ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix",
    "IAM_API_KEY": "yXZDE1xPrN2KF7m1kEvhm81GxUYz9Abo98b5--5z0Auk",
    "COUCH_URL": "https://ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix.cloudantnosqldb.appdomain.cloud",
    "state": "TX"
}

async function main() {
// async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
        if(params.state != null && params.state != ""){
            let state = params.state.toString();
            let data = cloudant.db.use('dealerships');
            let resultState = await data.find({ selector: { "state": state } });
            console.log(resultState.docs)
            if(resultState.docs.length > 0){
                return { "dealerships": resultState.docs };
            } else {
                let resultST = await data.find({ selector: { "st": state } });
                console.log(resultST.docs)
                if(resultST.docs.length > 0){
                    return { "dealerships": resultST.docs };
                } else {
                    return { "dealerships": []};
                }
            }
        } else {
             let dealerships = await new Promise(async resolve => {
                 let db = cloudant.db.use('dealerships');
                 let documents = await db.list({include_docs:true});
                 let results = []
                 if(documents.rows.length > 0){
                    for(let i = 0; i <= (documents.rows.length - 1); i++){
                        results.push(documents.rows[i].doc)
                    }
    
                    resolve(results)
                } else {
                    resolve([])
                }
             });
             
            return { "dealerships": dealerships};
        }
     } catch (error) {
         switch (error.statusCode) {
             case 404:
                return { error: "The database is empty" };
            case 500:
                return { error: "Something went wrong on the server" };
             default:
                return { error: error.description };
         }
     }
 
}

main()
