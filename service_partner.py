import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import requests
import boto3

region = 'us-east-2'  # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'search-kitoki-jyikzwreuzjtw4dvjqly6snq4y.us-east-2.es.amazonaws.com'
index = 'kitoki_service_partner'
url = 'https://' + host + '/' + index + '/_search'


def lambda_handler(event, context):
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    if event["home_page"] == 0:
        query = {
            "size": 25,
            "query": {
                "multi_match": {
                    "query": event["text"],
                    "type": "best_fields",
                    "fields": ["Company", "Address"],
                    "operator": "and"
                }
            }
        }
    else:
        query = {
            "size": 25,
            "query": {
                "match_all": {

                }
            }
        }

    # ES 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    return json.loads(r.text)