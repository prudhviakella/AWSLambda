import json
import requests
from ententparsing_product import get_product_intent_entity , get_service_intent_entity , get_newsfeed_intent_entity


def lambda_handler(event, context):

    headers = {"Content-Type": "application/json"}
    api_gateway_url = "https://jjemjsuloe.execute-api.us-east-2.amazonaws.com/Development/"
    aggregate_json = {}
    product_json = {}
    service_json = {}
    news_json = {}
    entity_json = {}
    intent_json = {}

    if int(event["product_flag"]) == 1:
        question = event["text"]
        intent_buying, entities , clean_question = get_product_intent_entity(question)
        entities_keywords = ' '.join(entities)
        entity_json['product'] = entities_keywords
        intent_json['product'] = intent_buying

        if intent_buying:
            product_response = requests.post(api_gateway_url + "product",
                                             data=json.dumps({"home_page": 0, "text": entities_keywords }))
            product_json_tmp = json.loads(product_response.text)

            if int(product_json_tmp["hits"]["total"]) > 0:
                product_json = {
                    "total": product_json_tmp["hits"]["total"],
                    "hits": product_json_tmp["hits"]["hits"]
                }

        else:
            product_response = requests.post(api_gateway_url + "product",
                                             data=json.dumps({"home_page": 0, "text": clean_question }))
            product_json_tmp = json.loads(product_response.text)
            if int(product_json_tmp["hits"]["total"]) > 0:
                product_json = {
                    "total": product_json_tmp["hits"]["total"],
                    "hits": product_json_tmp["hits"]["hits"]
                }

    if int(event["partner_service_flag"]) == 1:

        question = event["text"]
        intent_service , entities, clean_question = get_service_intent_entity(question)
        entities_keywords = ' '.join(entities)
        entity_json['service'] = entities_keywords
        intent_json['service'] = intent_service

        if intent_service:
            service_response = requests.post(api_gateway_url + "partner-services",
                                             data=json.dumps({"home_page": 0, "text": entities_keywords}))
            service_json_tmp = json.loads(service_response.text)

            if int(service_json_tmp["hits"]["total"]) > 0:
                product_json = {
                    "total": service_json_tmp["hits"]["total"],
                    "hits": service_json_tmp["hits"]["hits"]
                }

        else:
            service_response = requests.post(api_gateway_url + "partner-services",
                                             data=json.dumps({"home_page": 0, "text": clean_question}))
            service_json_tmp = json.loads(service_response.text)
            if int(service_json_tmp["hits"]["total"]) > 0:
                product_json = {
                    "total": service_json_tmp["hits"]["total"],
                    "hits": service_json_tmp["hits"]["hits"]
                }

    if int(event["newsfeed_flag"]) == 1:
        newsfeed_response = requests.post(api_gateway_url + "newsfeed",
                                          data=json.dumps({"home_page": 0, "text": event["text"]}))
        news_json_tmp = json.loads(newsfeed_response.text)
        if int(news_json_tmp["hits"]["total"]) > 0:
            news_json = {
                "total": news_json_tmp["hits"]["total"],
                "hits": news_json_tmp["hits"]["hits"]
            }


    aggregate_json['product'] = product_json
    aggregate_json['service_partner'] = service_json
    aggregate_json['newsfeeds'] = news_json
    aggregate_json['entity'] = entity_json
    aggregate_json['intent'] = intent_json

    return json.loads(json.dumps(aggregate_json))
