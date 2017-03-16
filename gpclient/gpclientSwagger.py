from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from gpclient import GPServiceAccount
from gpclient import GPClient
import requests
from pyswagger import App, Security
from pyswagger.contrib.client.requests import Client
from pyswagger.utils import jp_compose


class GPClientSwagger():
    def __init__(self):
        pass
if __name__ == '__main__':
    acc = GPServiceAccount(credentialsJson = "./test/data/local-credentials.json")
    client = GPClient(acc)
    http_client = RequestsClient()
    headers = client._GPClient__get_gaas_hmac_headers(  method="GET",
            url=None, date=None, body=None, secret=None, userId=None)
    url = acc.get_url() + '/swagger.json'

    
    swaggerClient = SwaggerClient.from_url(
        url,
        request_headers = headers
    )
    l = swaggerClient.service.getServiceInfo().result()
    print l
    from bravado.swagger_model import load_file
    #swaggerClient = SwaggerClient.from_spec(load_file('./swagger.json'))
    #l = swaggerClient.service.getServiceInfo().result()
    #print l
        #pet = client.pet.getPetById(petId=42).result()
#https://gp-rest.stage1.ng.bluemix.net/translate/rest/swagger.json
#{'GP-Date': 'Mon, 13 Mar 2017 17:58:45 GMT', 'Authorization': 'GP-HMAC #286bb08e66d36fb875a67a146517a597:7blwmSwsBaCGzoBvNuFMmDm2I0I='}
    
"""
{
  "url": "https://gp-test-rest.ng.bluemix.net/translate/rest",
  "userId": "4a299dc30ee95e3c7c6dbaa5c7ecaa62",
  "password": "aOG+GV2OTGtqjecL23N2y2pBbdm32fNp",
  "instanceId": "fb37c6071a9fba708a549a4b11aea6a6"
}
"""