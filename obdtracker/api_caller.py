import http3
import logging

from . import getapp
from . import utils

logger = logging.getLogger(__name__)

DEFAULT_HEADER = {'Content-Type': 'application/x-www-form-urlencoded'}


class ApiCaller():
    """
    This is base class for all requests to API. This class makes calls and 
    process responses.
    """
    __attrs__ = [
        'api_source', 'api_address', 'key', 'session', 'last_response'
    ]
    def __init__(self, server):
        """
        param: server: This is SERVER addres not API endpoint address
        """
        self.api_source = server
        self.api_address = getapp(self.api_source)
        self.key = None
        self.client = http3.AsyncClient()
        self.last_response = None

    async def getRequest(self, requestName, payload):
        """
        Process request, extracts required data and save it for next requests.
        Returns JSON object from response.

        param: requestName: It's a name of API endpoint
        param: payload: dict of params to be send to API endpoint
        """
        if '/' in requestName:
            requestName = str(requestName).replace('/','')

        self._addKey(requestName, payload)

        response = await self.client.get(
                    self.api_address+"/"+requestName,
                    params = payload,
                    headers = DEFAULT_HEADER
                )
        
        self.last_response = response

        if not response.status_code:
            raise Exception(message = response.content.decode() + response.headers)
        else:
            json = utils.getJSON(response.text)
            if requestName == "Login":
                self.key = json["deviceInfo"]["key2018"]

            return json

    def postRequest(self, requestName, payload):

        response = self.session.post(
                                    self.api_address + "/" + requestName,
                                    data = payload,
                                    headers = DEFAULT_HEADER
                                    )
        
        self.last_response = response
        return response

    def _addKey(self, requestName, payload):

        if requestName != 'Login' and "Key" not in payload:
            
            payload["Key"] = self.key
        
        return payload