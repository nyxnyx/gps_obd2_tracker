import requests
from . import getapp
from . import utils
from . import api_caller

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
        'battery',
        'batteryStatus',
        'course',
        'dataContext', 
        'deviceID',
        'deviceName',
        'ICCID',
        'icon',
        'id',
        'isGPS',
        'isStop',
        'lat',
        'lng',
        'model',
        'new201710',
        'ofl',
        'olat',
        'olng',
        'positionTime',
        'serialNumber',
        'sendCommand',
        'speed',
        'state',
        'status',
        'statusX20',
        'stm',
        'timeZone',
        'VIN',
        'voice',
        'warn',
        'warnStr',
        'warnTime',
        'warnTxt',
        'work',
        'xg',
        'yinshen'
    ]
    def __init__(self, server):

        super().__init__(server)
        self.app_address = getapp(server)
        self.language = "en"
    
    def doLogin(self, username, password):

        payload = { 'Name': username, 
                    'Pass': password, 
                    'LoginType': 1, 
                    'Key': APP_KEY
                    }

        json = self.getRequest('Login', payload)
        logger.debug("Got: %s", json)
        self.doSave(json)
    
    def doSave(self, response):

        if "deviceInfo" in response:
            response = response["deviceInfo"]

        for key in self.__attrs__:
            if key in response:
                v = response[key]
                if key in ['isGPS', 'isStop']:
                    v = (int(v) == 1)
                elif key in ['model', 'id', 'deviceID', 'xg']:
                    v = int(v)
                setattr(self, key, v)