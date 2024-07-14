from infra.requests_service import RequestsService
from infra.logger_config import logger


class OrderService:
    def __init__(self, requests_service: RequestsService) -> None:
        self.__requests = requests_service
        self.__endpoint = '/order'

    def cadastrar_pedido(self, product_ids: list, order_value: float, client_id: str):
        payload = {
            'value': order_value,
            'clientCpf': client_id,
            'productsIds': product_ids
        }
        response = self.__requests.post(endpoint=self.__endpoint, data=payload)
        logger.info(response)
        return response['resp']

    def atualizar_status_pedido(self, id_order: str, status: str):
        query_params = {
            'id': id_order,
            'status': status
        }
        response = self.__requests.put(endpoint=self.__endpoint, params=query_params)
        logger.info(response)
        return response