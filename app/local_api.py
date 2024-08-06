from flask import Flask, request, jsonify
import json
app = Flask(__name__)

# ClientService endpoints
@app.route('/client', methods=['POST'])
def cadastrar_cliente():
    client = request.json
    return jsonify({'statusCode': 201, 'body': json.dumps({'clientId': '123'})})

@app.route('/client/client_id', methods=['GET'])
def consultar_cliente_por_cpf():
    cpf = request.args.get('id')
    if cpf == '23144234565':
        return jsonify({'resp': {'statusCode': 200, 'body': json.dumps({'clientId': '123'})}})
    return jsonify({'resp':{'statusCode': 404, 'body': 'Cliente não encontrado'}}), 404

# OrderService endpoints
@app.route('/order', methods=['POST'])
def cadastrar_pedido():
    order = request.json
    return jsonify({'resp': {'statusCode': 201, 'body': json.dumps({'orderId': '456'})}})

@app.route('/order', methods=['PUT'])
def atualizar_status_pedido():
    id_order = request.args.get('id')
    status = request.args.get('status')
    return jsonify({'resp': {'statusCode': 200, 'body': 'Pedido atualizado com sucesso'}})

# PaymentService endpoints
@app.route('/payment', methods=['POST'])
def realizar_pagamento():
    payment = request.json
    return jsonify({'statusCode': 200, 'body': 'Pagamento realizado com sucesso'})

@app.route('/payment', methods=['PUT'])
def realizar_estorno():
    refund = request.json
    return jsonify({'statusCode': 200, 'body': 'Pagamento estornado com sucesso'})

# KitchenService endpoints
@app.route('/kitchen/order-status', methods=['PUT'])
def enviar_pedido_para_cozinha():
    kitchen = request.json
    return jsonify({'resp': {'statusCode': 200, 'body': 'Pedido enviado para a cozinha com sucesso'}})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
