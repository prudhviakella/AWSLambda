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
index = 'newsfeed'
url = 'https://' + host + '/' + index + '/_search'


def lambda_handler(event, context):
    aggregate_json = {}
    product_json = {}
    service_json = {}
    news_json = {}
    if event["home_page"] == 0:
        query = {
            "size": 25,
            "query": {
                "multi_match": {
                    "query": event["text"],
                    "type": "best_fields",
                    "fields": ["title", "Description"],
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
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    return json.loads(r.text)


