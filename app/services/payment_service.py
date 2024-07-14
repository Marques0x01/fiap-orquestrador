from infra.requests_service import RequestsService
from infra.logger_config import logger

class PaymentService:
    def __init__(self, requests_service: RequestsService) -> None:
        self.__requests = requests_service
        self.__endpoint = '/payment'

    def realizar_pagamento(self, id_client: str, id_order: str, payment_value: str, payment_method: str='MERCADO PAGO'):
        payload = {
            'id_cliente': id_client,
            'id_pedido': id_order,
            'tipo_pagamento': payment_method,
            'valor_pagamento': payment_value
        }
        response = self.__requests.post(endpoint=self.__endpoint, data=payload)
        logger.info(response)
        return response

    def realizar_estorno(self, id_client: str, id_order: str, motivo_estorno: str):
        payload = {
            'id_cliente': id_client,
            'id_pedido': id_order,
            'motivo_estorno': motivo_estorno
        }
        response = self.__requests.put(endpoint=self.__endpoint, data=payload)
        logger.info(response)
        return response
