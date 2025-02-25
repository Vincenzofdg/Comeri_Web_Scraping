import requests
import json

urls = {
    "product": "https://3z8dyfct87.execute-api.sa-east-1.amazonaws.com/main/products?environment=production&establishmentId=",
}

def request_aws_get(endpoint, client_id):
    try:
        request_action = requests.get(urls[endpoint] + client_id)
        request_to_json = json.loads(request_action.text)
        resquest_body =  json.loads(request_to_json.get('body', {}))

        data = resquest_body.get('data', [])
        return data
    except requests.exceptions.RequestException as error:
        print(error)
        return []