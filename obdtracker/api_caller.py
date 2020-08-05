import http3
import logging
import asyncio
import xml.etree.ElementTree
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
        'api_source', 'api_address', 'key', 'client', 'last_response'
    ]
    def __init__(self, server):
        """
        param: server: This is SERVER addres not API endpoint address
        """
        self.api_source = server
        self.api_address = getapp(self.api_source)
        self.key = None
        self.id = None
        self.last_response = None

    async def connect(self):
        self.client = http3.AsyncClient()

    async def getRequest(self, requestName, payload):
        """
        Process request, extracts required data and save it for next requests.
        Returns JSON object from response.

        param: requestName: It's a name of API endpoint
        param: payload: dict of params to be send to API endpoint
        """
        if not hasattr(self, "client"):
            await self.connect()

        if '/' in requestName:
            requestName = str(requestName).replace('/','')

        self._addKey(requestName, payload)
        if self.id is None and "DeviceID" in payload:
            self.id = payload["DeviceID"]
            logger.info("Saving ID: %s" % self.id)
        response = await self.client.get(
                    self.api_address+"/"+requestName,
                    params = payload,
                    headers = DEFAULT_HEADER
                )
        
        self.last_response = response
        json = None
        if not response.status_code:
            raise Exception(message = response.content.decode() + response.headers)
        elif len(response.content) == 0:
            logger.debug("Content length is 0")
        else:
            try:
                json = utils.getJSON(response.text)
            except xml.etree.ElementTree.ParseError as e:
                logger.debug(F"Can't parse response {len(response.content)}")

            if requestName == "Login":
                self.key = json["deviceInfo"]["key2018"]

            return json

    async def postRequest(self, requestName, payload):

        if not hasattr(self, "client"):
            await self.connect()

        response = self.client.post(
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
    
    def __del__(self):
        asyncio.ensure_future(self.getRequest("ExitAndroid", payload={"ID": self.id, "TypeID": "1", "Key": self.key } ) )
        logger.info("Destructor")