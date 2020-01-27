import logging
from . import login_action

logger = logging.getLogger(__name__)

class DeviceStatus:

    def __init__(self, loginAction):

        self._la = loginAction
    
    def get_device_status(self):

        payload = {
            "DeviceID": self._la._deviceID,
            "TimeZones": self._la._timeZone,
            "Language": "pl_PL",
            "FilterWarn": ""
        }
        _set_device_status(self._la.getRequest("GetDeviceStatus", payload))

    def get_device_status2_by_DDC(self):
            
        payload = {
            "DeviceID": self._la._deviceID,
            "Language": "pl_PL"
        }
        json = self._la.getRequest("GetDeviceStatus2ByDDC", payload)
        logger.debug(json)
        self._la._state = json("state")
        
    def get_device_status_FZE(self):
        payload = {
            "DeviceID": self._la._deviceID,
            "TimeZones": self._la._timeZone,
            "Language": "pl_PL",
            "FilterWarn": ""
        }
        json = self._la.getRequest("GetDeviceStatusFZE", payload)
        logger.debug(json)

        def _set_device_status(self, json):
            here = self._la
            here._state = json["state"]
            here._id = json["id"]
            here._yinshen = json["yinshen"]
            here._sendCommand = json["sendCommand"]
            here._voice = json["voice"]
            here._warnTxt = json["warnTxt"]
            here._warnTime = json["warnTime"]
            here._dataContext = json["dataContext"]
            here._battery = json["battery"]
            here._batteryStatus = json["batteryStatus"]
            here._statusX20 = json["statusX20"]