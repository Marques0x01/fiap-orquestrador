from infra.requests_service import RequestsService
from infra.logger_config import logger

class KitchenService:
    def __init__(self, requests_service: RequestsService) -> None:
        self.__requests = requests_service
        self.__endpoint = '/kitchen/order-status'

    def enviar_pedido_para_cozinha(self, id_order: str, id_client: str, status_order: str='preparing'):
        payload = {
            'id': id_order,
            'status': status_order,
            'client_id': id_client
        }
        response = self.__requests.put(endpoint=self.__endpoint, data=payload)
        logger.info(response)
        return response['resp']
