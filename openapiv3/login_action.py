import requests
from . import getapp, APP_KEY
from . import utils

import logging



class LoginAction:
    '''LoginAction - class used to perform login action '''
    
    def __init__(self, host):
        self.logger = logging.getLogger(__name__)
        self._key2018 = ''
        self._app_address = getapp(host)
    
    def doLogin(self, username, password) -> bool:
        payload = { 'Name': username, 
                    'Pass': password, 
                    'LoginType': 1, 
                    'Key': APP_KEY
                    }
        url = "%s/%s" % (self._app_address, "Login")
        print (url)
        r = requests.get(url=url, 
                        params=payload,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'}
                        )
        self.logger.debug("Got: %s", r.content.decode())
        return self._checkResponse(r)
    
    def _checkResponse(self, response) -> bool:

        if not response.ok:
            return False
        else:
            
            self._login_data = utils.getJSON(response.content)
            deviceInfo = self._login_data["deviceInfo"]

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
            self._key2018 = deviceInfo["key2018"]
            self.logger.debug("key2018: %s", deviceInfo["key2018"])

    def getKey2018(self) -> str:
        return self._key2018

    def getAddress(self) -> str:

        return self._app_address