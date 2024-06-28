import requests
import json


class HttpService:

    app = "http://fiap-elb-1174290082.us-east-1.elb.amazonaws.com:3000/api/v1"

    gtw = "https://104kqew899.execute-api.us-east-1.amazonaws.com/prod/fiap-lanches"

    def create_order(self, order: dict):
        headers = {
            'Content-Type': 'application/json'
        }

        request_order = {
            "value": order.get("value"),
            "productsIds": order.get("productsIds"),
            "clientCpf": order.get("client").get("cpf")
        }

        result_creation = requests.post(self.gtw+"/order",
                                        data=json.dumps(request_order), headers=headers)

        if (result_creation.status_code != 200):
            raise Exception("Error on creating order")

        result_body: dict = json.loads(result_creation.text)
        result_response: dict = result_body.get("resp")
        return json.loads(result_response.get("body"))

    def create_client(self, data: dict):
        result_get = requests.get(
            self.app+"/client/"+data.get("client").get("cpf"))

        if (result_get.status_code != 200):
            raise Exception("Error on getting client")

        if (result_get.status_code == 200):
            return

        if (result_get.status_code == 404):
            headers = {
                'Content-Type': 'application/json'
            }

            result_post = requests.post(
                self.app+"/client", headers=headers, data=json.dumps(data.get("client")))
            
            if(result_post.status_code == 409):
                return
            
            if(result_post.status_code != 200):
                raise Exception("Error on creating order")
                
