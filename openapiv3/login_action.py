import requests
from . import getapp, APP_KEY
from . import utils
from . import api_caller

import logging



class LoginAction(api_caller.ApiCaller):
    '''LoginAction - class used to perform login action '''
    
    def __init__(self, host):

        super().__init__(host)
        self.logger = logging.getLogger(__name__)
        self._key2018 = ''
        self._app_address = getapp(host)
    
    def doLogin(self, username, password) -> bool:
        payload = { 'Name': username, 
                    'Pass': password, 
                    'LoginType': 1, 
                    'Key': APP_KEY
                    }

        json = self.getRequest('Login', payload)
        self.logger.debug("Got: %s", json)
        return self._checkResponse(json)
    
    def _checkResponse(self, response) -> bool:

        deviceInfo = response["deviceInfo"]
        self._deviceID = deviceInfo["deviceID"]
        self._model = deviceInfo["model"]
        self._serialNumber = deviceInfo["sn"]
        self._sendCommand = deviceInfo["sendCommand"]
        self._voice = deviceInfo["voice"]
        self._deviceName = deviceInfo["deviceName"]
        self._warnStr = deviceInfo["warnStr"]
        self._timeZone = deviceInfo["timeZone"]
        self._new201710 = deviceInfo["new201710"]
        self._icon = deviceInfo["icon"]

    def getKey2018(self) -> str:
        return self._key2018

    def getAddress(self) -> str:

        return self._app_address