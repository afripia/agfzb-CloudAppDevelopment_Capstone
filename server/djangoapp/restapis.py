import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, api_key = None, **kwargs):
    try:
        # Call get method of requests library with URL and parameters
        if api_key is None :
            response = requests.get(
                url,
                headers={'Content-Type': 'application/json'},
                params=kwargs
            )
        else:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(
                url,
                params=params,
                headers={'Content-Type': 'application/json'},
                auth=HTTPBasicAuth('apikey', api_key)
            )

    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=payload)

    except:
        # If any error occurs
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    if "state" in kwargs :
        json_result = get_request(url, None, state=kwargs['state'])
    else :
        json_result = get_request(url, None)

    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealerships"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                address=dealer["address"],
                city=dealer["city"],
                full_name=dealer["full_name"],
                id=dealer["id"],
                lat=dealer["lat"],
                long=dealer["long"],
                short_name=dealer["short_name"],
                st=dealer["st"],
                state=dealer["state"],
                zip=dealer["zip"]
            )

            results.append(dealer_obj)

    return results

# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_by_id_from_cf(url, **kwargs):
    result = None
    # Call get_request with a URL parameter
    json_result = get_request(url, None, dealerId=kwargs['dealerId'])
    if json_result:
        dealer = json_result["dealerships"][0]
        dealer_obj = CarDealer(
            address=dealer["address"],
            city=dealer["city"],
            full_name=dealer["full_name"],
            id=dealer["id"],
            lat=dealer["lat"],
            long=dealer["long"],
            short_name=dealer["short_name"],
            st=dealer["st"],
            state=dealer["state"],
            zip=dealer["zip"]
        )

        result = dealer_obj

    return result

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, None, dealerId=kwargs['dealerId'])
    if json_result:
        dealer_reviews = json_result["reviews"]
        for dealer_review in dealer_reviews:
            dealer_review_obj = DealerReview(
                # id = dealer_review['_id'],
                name = dealer_review['name'],
                dealership = dealer_review['dealership'],
                review = dealer_review['review'],
                purchase = dealer_review['purchase'] if dealer_review['purchase'] else None,
                purchase_date = dealer_review['purchase_date'] if dealer_review['purchase'] else None,
                car_make = dealer_review['car_make'] if dealer_review['purchase'] else None,
                car_model = dealer_review['car_model'] if dealer_review['purchase'] else None,
                car_year = dealer_review['car_year'] if dealer_review['purchase'] else None,
                sentiment = None
            )

            dealer_review_obj.sentiment = analyze_review_sentiments(dealer_review['review'])

            results.append(dealer_review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    try:
        url = 'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/63de4ccf-6fba-4143-88b4-cdf3f685f284/v1/analyze'
        api_key = 'K2UdcPhYqjHRiciiAZI5ApZaKaVZ61XJZ19fa8SpDy5c'

        json_result = get_request(
            url,
            api_key,
            text = dealerreview,
            version = '2021-08-01',
            features = {
                "sentiment": {}
            },
            return_analyzed_text = False
        )

        return json_result['sentiment']['document']['label']
    except:
        return "None"