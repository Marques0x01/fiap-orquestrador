from infra.requests_service import RequestsService
from infra.logger_config import logger
class ClientService:
    def __init__(self, request_service: RequestsService) -> None:
        self.__requests = request_service
        self.__endpoint = '/client'

    def cadastrar_cliente(self, client: dict):
        response = self.__requests.post(endpoint=self.__endpoint, data=client)
        logger.info(response)
        return response['resp']

    def consultar_cliente_por_cpf(self, cpf: str):
        query_params = {'id': cpf}
        response = self.__requests.get(endpoint=f'{self.__endpoint}/client_id', params=query_params)
        return response['resp']