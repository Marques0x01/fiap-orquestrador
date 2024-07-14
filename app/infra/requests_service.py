import requests
import json
from infra.logger_config import logger

class RequestsService:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers if headers else {'Content-Type': 'application/json'}

    def get(self, endpoint: str, params: dict = None) -> dict:
        url = f'{self.base_url}{endpoint}'
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint: str, data: dict) -> dict:
        url = f'{self.base_url}{endpoint}'
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return self._handle_response(response)

    def put(self, endpoint: str, data: dict = {}, params: dict = None) -> dict:
        url = f'{self.base_url}{endpoint}'
        response = requests.put(url, headers=self.headers, data=json.dumps(data), params=params)
        return self._handle_response(response)

    def delete(self, endpoint: str) -> dict:
        url = f'{self.base_url}{endpoint}'
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        try:
            response.raise_for_status()
            logger.info(f'Status Code: {response.status_code}, Response: {response.json()}')
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred: {http_err} - Response: {response.text}')
            return {'statusCode': response.status_code, 'body': response.text}
        except Exception as err:
            logger.error(f'Other error occurred: {err}')
            return {'statusCode': 500, 'body': str(err)}