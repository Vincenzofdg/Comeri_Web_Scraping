import requests

urls = {
    "product": "https://3z8dyfct87.execute-api.sa-east-1.amazonaws.com/main/products?environment=production&",
}

def request_aws_post(endpoint, data):
    try:
        requests.post(urls[endpoint], json=data)
        # print(
        #     f'\nName: {data["name"]}\nCategory: {data["categoryId"]}')
        return f'{data["name"]} successfully created'
    except requests.exceptions.RequestException as error:
        print("Err: ", error)
        return