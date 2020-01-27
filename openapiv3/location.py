import logging
from . import login_action

logger = logging.getLogger(__name__)

class Location:

    def __init__(self, loginAction):

        self._la = loginAction

    def getTracking(self):

        payload = {
            "DeviceID": self._la._deviceID,
            "Model": self._la._model,
            "TimeZones": self._la._timeZone,
            "MapType": "Google",
            "Language": "pl_PL"
        }

        json = self._la.getRequest("GetTracking", payload)
        logger.debug(json)
        self._doSave(json)

    def _doSave(self, json):

        here = self._la

        here._state         = json['state']
        here._positionTime  = json['positionTime']
        here._lat           = json['lat']
        here._lng           = json['lng']
        here._ofl           = json['ofl']
        here._olat          = json['olat']
        here._olng          = json['olng']
        here._speed         = json['speed']
        here._course        = json['course']
        here._isStop        = int(json['isStop']) == 1
        here._icon          = json['icon']
        here._isGPS         = int(json['isGPS']) == 1
        here._ICCID         = json['ICCID']
        here._VIN           = json['VIN']
        here._stm           = json['stm']
        here._warn          = json['warn']
        here._work          = json['work']
        here._battery       = json['battery']
        here._batteryStatus = json['batteryStatus']
        here._status        = json['status']
        here._statusX20     = json['statusX20']