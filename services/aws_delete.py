import requests

urls = {
    "product": "https://3z8dyfct87.execute-api.sa-east-1.amazonaws.com/main/products?environment=production&delete=",
}

headers = {"Content-Type": "application/json"}

def request_aws_delete(endpoint, id_to_delete):
    try:
        requests.delete(urls[endpoint] + id_to_delete)
        return f'{id_to_delete} successfully deleted'
    except requests.exceptions.RequestException as error:
        print("Err: ", error)
        return