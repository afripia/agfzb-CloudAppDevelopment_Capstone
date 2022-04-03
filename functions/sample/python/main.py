#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

dict = {
    "COUCH_USERNAME": "ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix",
    "IAM_API_KEY": "yXZDE1xPrN2KF7m1kEvhm81GxUYz9Abo98b5--5z0Auk",
    "COUCH_URL": "https://ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix.cloudantnosqldb.appdomain.cloud",
    "dealerId": "2"
}

def main(dict):
    try:
        IAM_API_KEY = dict["IAM_API_KEY"]
        COUCH_URL = dict["COUCH_URL"]
        
        databaseName = "reviews"
        
        authenticator = IAMAuthenticator(IAM_API_KEY)
        client = CloudantV1(authenticator=authenticator)
        client.set_service_url(COUCH_URL)
        
        response = client.post_find(
        db='reviews',
        selector={'id': {'$eq': int(dict['dealerId'])}},
        ).get_result()
        
        return {'reviews': response['docs']}
    
    except ApiException as ae:
        if ae.code == 404:
            return {
                'statusCode': 404,
                'message': 'dealerId does not exist'
            }
        elif ae.code == 500:
            return {
                'statusCode': 404,
                'message': 'Something went wrong on the server'
            }
        else :
            return {
                'statusCode': ae.code,
                'message': ae.message
            }
