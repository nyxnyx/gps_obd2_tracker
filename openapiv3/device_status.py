import logging
import requests
from . import login_action, utils

logger = logging.getLogger(__name__)

class DeviceStatus:

    def __init__(self, loginAction):
        
        if loginAction.getKey2018() == "":
            logger.error("No Key2018!!! Did you logged in?")
        else:
            self._la = loginAction
    
    def get_device_status(self):

        payload = {
            "DeviceID": self._la._deviceID,
            "TimeZones": self._la._timeZone,
            "Language": "pl_PL",
            "FilterWarn": "",
            "Key": self._la._key2018
        }
        r = requests.get(self._la.getAddress() + "/GetDeviceStatus",
                    params = payload,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                    )

        logger.debug(r.content.decode())
        _set_device_status(utils.getJSON(r.content.decode()))

    def get_device_status2_by_DDC(self):
            
        payload = {
            "DeviceID": self._la._deviceID,
            "Language": "pl_PL",
            "Key": self._la._key2018
        }
        r = requests.get(self._la.getAddress() + "/GetDeviceStatus2ByDDC",
                params = payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
        json = utils.getJSON(r.content.decode())
        logger.debug(json)
        self._state = json("state")
        
    def get_device_status_FZE(self):
        payload = {
            "DeviceID": self._la._deviceID,
            "TimeZones": self._la._timeZone,
            "Language": "pl_PL",
            "FilterWarn": "",
            "Key": self._la._key2018
        }
        r = requests.get(self._la.getAddress() + "/GetDeviceStatusFZE",
                params = payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
        json = utils.getJSON(r.content.decode())
        logger.debug(json)

        def _set_device_status(self, json):
            self._state = json["state"]
            self._id = json["id"]
            self._yinshen = json["yinshen"]
            self._sendCommand = json["sendCommand"]
            self._voice = json["voice"]
            self._warnTxt = json["warnTxt"]
            self._warnTime = json["warnTime"]
            self._dataContext = json["dataContext"]
            self._battery = json["battery"]
            self._batteryStatus = json["batteryStatus"]
            self._statusX20 = json["statusX20"]