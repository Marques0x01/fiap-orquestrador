import json
from infra.logger_config import logger
from infra.requests_service import RequestsService
from services.client_service import ClientService
from services.order_service import OrderService
from services.payment_service import PaymentService
from services.kitchen_service import KitchenService

# provisionamento de recursos globais do lambda
try:
    req = RequestsService('https://g5sd3oe22m.execute-api.us-east-2.amazonaws.com/prod/fiap-lanches')
    client_service = ClientService(req)
    order_service = OrderService(req)
    payment_service = PaymentService(req)
    kitchen_service = KitchenService(req)
except Exception as ex:
    raise ex

class SagaException(Exception):
    pass

class Saga:
    def __init__(self):
        self.steps = []
        self.compensations = []

    def add_step(self, step, compensation):
        self.steps.append(step)
        self.compensations.append(compensation)

    def execute(self):
        for i, step in enumerate(self.steps):
            try:
                step()
            except Exception as e:
                logger.error(f"Erro no passo {i + 1}: {e}")
                self.rollback(i)
                raise SagaException(f"Saga falhou no passo {i + 1}: {e}")

    def rollback(self, failed_step):
        for i in range(failed_step, -1, -1):
            try:
                self.compensations[i]()
            except Exception as e:
                logger.error(f"Erro na compensação do passo {i + 1}: {e}")

def lambda_handler(event, context):
    id_pedido = None
    id_cliente = None
    mensagens = event['Records']
    logger.info(mensagens)
    if len(mensagens) == 0:
        return {'message': 'lambda finalizado pois não existem mensagens a serem lidas'}
    
    for mensagem in mensagens:
        item = json.loads(mensagem['body'])
        
        saga = Saga()
        
        try:
            '''
            Etapa de consulta e criação de cliente
            '''
            def consultar_cliente():
                nonlocal id_cliente
                if item.get('register') is True:
                    result_get_client = client_service.consultar_cliente_por_cpf(item['client']['cpf'])
                    if result_get_client['statusCode'] != 200:
                        result_register_client = client_service.cadastrar_cliente(item['client'])
                        if result_register_client['statusCode'] != 201:
                            raise Exception(f'Erro ao cadastrar cliente: {result_register_client}')
                        id_cliente = json.loads(result_register_client['body'])['clientId']
                    else:
                        id_cliente = json.loads(result_get_client['body'])['clientId']
                else:
                    id_cliente = 'TEMP_CLIENT'

            def compensar_cliente():
                if id_cliente and id_cliente != 'TEMP_CLIENT':
                    # Não é necessário excluir o cliente >:^)
                    pass
            
            saga.add_step(consultar_cliente, compensar_cliente)
            
            '''
            Etapa de criação de pedido
            '''
            def criar_pedido():
                nonlocal id_pedido
                result_register_order = order_service.cadastrar_pedido(item['productsIds'], item['value'], item['client']['cpf'])
                if result_register_order['statusCode'] != 201:
                    raise Exception(f'Erro ao cadastrar pedido: {result_register_order}')
                id_pedido = json.loads(result_register_order['body'])['orderId']
            
            def compensar_pedido():
                if id_pedido:
                    order_service.atualizar_status_pedido(id_pedido, 'CANCELADO')
                    logger.info(f'Pedido {id_pedido} cancelado devido a erro.')
            
            saga.add_step(criar_pedido, compensar_pedido)
            
            '''
            Etapa de pagamento
            '''
            def realizar_pagamento():
                result_payment = payment_service.realizar_pagamento(id_cliente, id_pedido, item['value'])
                if result_payment['statusCode'] != 200:
                    raise Exception(f'Erro ao realizar pagamento: {result_payment}')

            def compensar_pagamento():
                if id_pedido:
                    payment_service.estornar_pagamento(id_cliente, id_pedido, item['value'])
                    logger.info(f'Pagamento do pedido {id_pedido} estornado devido a erro.')
            
            saga.add_step(realizar_pagamento, compensar_pagamento)
            
            '''
            Etapa Cozinha
            '''
            def enviar_para_cozinha():
                result_kitchen = kitchen_service.enviar_pedido_para_cozinha(id_pedido, id_cliente)
                if result_kitchen['statusCode'] != 200:
                    raise Exception(f'Erro ao enviar pedido para a cozinha: {result_kitchen}')

            def compensar_cozinha():
                # Adicione a lógica de compensação para a cozinha, se necessário
                pass
            
            saga.add_step(enviar_para_cozinha, compensar_cozinha)
            
            saga.execute()

        except SagaException as e:
            return {'statusCode': 500, 'body': json.dumps({'message': str(e)})}

    return {'statusCode': 200, 'body': json.dumps({'message': 'Processamento concluído com sucesso'})}
