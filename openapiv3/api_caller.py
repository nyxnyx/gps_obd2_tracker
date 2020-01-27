import requests
import logging
from . import getapp, APP_KEY
from . import utils

logger = logging.getLogger(__name__)


class ApiCaller():

    def __init__(self, host):

        self._api_source = host
        self._api_address = self._ask_for_api_address(host)
        self._key = ""

    def _ask_for_api_address(self, host) -> str:

        return getapp(host)

    def getRequest(self, requestName, payload):

        if requestName != 'Login' and "Key" not in payload:
            payload["Key"] = self._key

        response = requests.get(
                    self._api_address+"/"+requestName,
                    params = payload,
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                )
        if not response.ok:
            raise Exception(message = response.content.decode())
        else:
            json = utils.getJSON(response.content.decode())
            if requestName == "Login":
                self._key = json["deviceInfo"]["key2018"]

            return json
