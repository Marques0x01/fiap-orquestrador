from lambda_function import lambda_handler

payload = {
    'Records': [
        {
            'body': "{\"value\": 100,\"register\": true,\"productsIds\": [\"19e61598-3147-49e3-a42a-def44390846c\"],\"client\": {\"cpf\": \"23144234565\",\"name\": \"nome completo\",\"email\": \"nome@completo.com\"}}"
        }
    ]
}
lambda_handler(payload, None)