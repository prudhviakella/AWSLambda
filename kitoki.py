import json
import requests


def lambda_handler(event, context):
    headers = {"Content-Type": "application/json"}
    api_gateway_url = "https://jjemjsuloe.execute-api.us-east-2.amazonaws.com/Development/"
    aggregate_json = {}
    product_json = {}
    service_json = {}
    news_json = {}


    if int(event["product_flag"]) == 1:
        if event["home_page"] == 0:
            product_response = requests.post(api_gateway_url + "product", data=json.dumps({"home_page": 0, "text": event["text"]}))
        else:
            product_response = requests.post(api_gateway_url + "product",
                                             data=json.dumps({"home_page": 1, "text": event["text"]}))
        product_json_tmp = json.loads(product_response.text)
        if int(product_json_tmp["hits"]["total"]) > 0:
            product_json = {
                "total": product_json_tmp["hits"]["total"],
                "hits": product_json_tmp["hits"]["hits"]
            }

    if int(event["partner_service_flag"]) == 1:
        if event["home_page"] == 0:
            service_response = requests.post(api_gateway_url + "partner-services",
                                             data=json.dumps({"home_page": 0,"text": event["text"]}))
        else:
            service_response = requests.post(api_gateway_url + "partner-services",
                                             data=json.dumps({"home_page": 1, "text": event["text"]}))
        service_json_tmp = json.loads(service_response.text)
        if int(service_json_tmp["hits"]["total"]) > 0:
            service_json = {
                "total": service_json_tmp["hits"]["total"],
                "hits": service_json_tmp["hits"]["hits"]
            }

    if int(event["newsfeed_flag"]) == 1:
        if event["home_page"] == 0:
            newsfeed_response = requests.post(api_gateway_url + "newsfeed",
                                              data=json.dumps({"home_page": 0, "text": event["text"]}))
        else:
            newsfeed_response = requests.post(api_gateway_url + "newsfeed",
                                              data=json.dumps({"home_page": 1, "text": event["text"]}))
        news_json_tmp = json.loads(newsfeed_response.text)
        if int(news_json_tmp["hits"]["total"]) > 0:
            news_json = {
                "total": news_json_tmp["hits"]["total"],
                "hits": news_json_tmp["hits"]["hits"]
            }


    aggregate_json['product'] = product_json
    aggregate_json['service_partner'] = service_json
    aggregate_json['newsfeeds'] = news_json
    aggregate_json['intent'] = "Workinprogress"

    return json.loads(json.dumps(aggregate_json))
