from . import getapp
from . import utils
from . import api_caller
from . import updater
import time

import logging
logger = logging.getLogger(__name__)

APP_KEY = '7DU2DJFDR8321'

class API(api_caller.ApiCaller):
    """
    LoginAction - class used to perform login action and store all information from
    different API calls. Options available after calling actions are availabe in __attrs__
    table.
    """
    
    __attrs__ = [
        'app_address',
        'battery', # GetTracking, GetDeviceStatus, GetDeviceStatusFZE
        'batteryStatus', # GetTracking, GetDeviceStatus, GetDeviceStatusFZE
        'course', # GetTracking
        'dataContext', # GetDeviceStatus, GetDeviceStatusFZE
        'deviceID', # Login
        'deviceName', # Login
        'ICCID', # GetTracking
        'icon', # Login, GetTracking
        'id', # GetDeviceStatus, GetDeviceStatusFZE
        'isGPS', # GetTracking
        'isStop', # GetTracking
        'key2018', # Login
        'lat', # GetTracking
        'lng', # GetTracking
        'model', # Login
        'new201710', # Login
        'ofl', # GetTracking
        'olat', # GetTracking
        'olng', # GetTracking
        'positionTime', # GetTracking
        'serialNumber',
        'sendCommand', # Login, GetDeviceStatus, GetDeviceStatusFZE
        'speed', # GetTracking
        'sn', # Login
        'state', # Login, GetTracking, GetDeviceStatus, GetDeviceStatus2ByDDC, GetDeviceStatusFZE
        'status', # GetTracking, GetDeviceStatus, GetDeviceStatusFZE
        'statusX20', # GetTracking, GetDeviceStatus, GetDeviceStatusFZE
        'stm', # GetTracking
        'timeZone', # Login
        'VIN', # GetTracking
        'voice', # Login, GetDeviceStatus, GetDeviceStatusFZE
        'warn', # GetTracking
        'warnStr', # Login
        'warnTime', # GetDeviceStatus, GetDeviceStatusFZE
        'warnTxt', # GetDeviceStatus, GetDeviceStatusFZE
        'work', # GetTracking
        'xg', # Login
        'yinshen' # GetDeviceStatus, GetDeviceStatusFZE
    ]

    INT_DATA = ['model', 'id', 'deviceID']
    BOOL_DATA = ['isGPS', 'isStop', 'xg', 'icon', 'new201710', 'voice']
    updaters = []
    
    def __init__(self, server):

        super().__init__(server)
        self.app_address = getapp(server)
        self.language = "en"
    
    async def doLogin(self, username, password):

        payload = { 'Name': username,
                    'Pass': password,
                    'LoginType': 1,
                    'LoginAPP': "AKSH",
                    'GMT': "2:00",
                    'Key': APP_KEY
                    }

        json = await self.getRequest('Login', payload)
        logger.debug("doLogin: %s", json)
        self.doSave(json)
    
    def doSave(self, response):

        if "deviceInfo" in response:
            response = response["deviceInfo"]

        for key in self.__attrs__:
            if key in response:
                v = response[key]
                if key in self.BOOL_DATA:
                    v = (int(v) == 1)
                elif key in self.INT_DATA:
                    v = int(v)
                setattr(self, key, v)

    async def doUpdate(self):
        if len(self.updaters) > 0:
            for u in self.updaters:
                await u.update()

    def registerUpdater(self, interface):
        if isinstance(interface, updater.isUpdater):
            self.updaters.append(interface)    