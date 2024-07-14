import json
from infra.logger_config import logger
from infra.requests_service import RequestsService
from services.client_service import ClientService
from services.order_service import OrderService
from services.payment_service import PaymentService

# provisionamento de recursos globais do lambda
req = RequestsService('https://g5sd3oe22m.execute-api.us-east-2.amazonaws.com/prod/fiap-lanches')
client_service = ClientService(req)
order_service = OrderService(req)
payment_service = PaymentService(req)

def lambda_handler(event, context):
    id_pedido = None
    id_cliente = None
    mensagens = event['Records']
    logger.info(mensagens)
    if len(mensagens) == 0:
        return {'message': 'lambda finalizado pois não existem mensagens a serem lidas'}
    for mensagem in mensagens:
        item = json.loads(mensagem['body'])
        '''
        Etapa de consulta e criação de cliente
        '''
        if item.get('register') is True:
            result_get_client = client_service.consultar_cliente_por_cpf(item['client']['cpf'])
            if result_get_client['statusCode'] != 200:
                result_register_client = client_service.cadastrar_cliente(item['client'])
                if result_register_client['statusCode'] != 201:
                    # TODO: criar funcionalidade de notificação
                    raise Exception(f'Erro ao cadastrar cliente: {result_register_client}')
                id_cliente = json.loads(result_register_client['body'])['clientId']
        else:
            id_cliente = 'TEMP_CLIENT'
        '''
        Etapa de criação de pedido
        '''
        result_register_order = order_service.cadastrar_pedido(item['productsIds'], item['value'], item['client']['cpf'])
        if result_register_order['statusCode'] != 201:
            # TODO: criar funcionalidade de notificação
            raise Exception(f'Erro ao cadastrar pedido: {result_register_order}')
        id_pedido = json.loads(result_register_order['body'])['orderId']
        '''
        Etapa de pagamento
        '''
        result_payment = payment_service.realizar_pagamento(id_cliente, id_pedido, item['value'])
        if result_payment['statusCode'] != 200:
            order_service.atualizar_status_pedido(id_pedido, 'CANCELADO')
        '''
        Etapa Cozinha
        '''
        return {'statusCode': 500, 'body': json.dumps({'message': 'sensibilização da cozinha ainda não implementada'})}
