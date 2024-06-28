import json

from infra.HttpService import HttpService


httpService = HttpService()

def lambda_handler(event, context):
    try:
        
        data = json.loads(event['body'])

        httpService.create_client(data)
        httpService.create_order(data)
        
    except ValueError:
        # notificarClient()
        return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON'})}
    


with open('massa.json', 'r') as file:
    obj = json.load(file)

lambda_handler(obj, None)