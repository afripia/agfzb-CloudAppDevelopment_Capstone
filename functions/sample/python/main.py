#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

dict = {
    "COUCH_USERNAME": "ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix",
    "IAM_API_KEY": "yXZDE1xPrN2KF7m1kEvhm81GxUYz9Abo98b5--5z0Auk",
    "COUCH_URL": "https://ceeedc5c-ae97-4b49-8621-08f97ef9c50d-bluemix.cloudantnosqldb.appdomain.cloud"
}

# def main(dict):
def main():
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            url=dict["COUCH_URL"],
            connect=True,
        )
        my_database = client[databaseName]
        # print("Databases: {0}".format(client.all_dbs()))
        # return {"dbs": client.all_dbs()}
        return my_database
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
