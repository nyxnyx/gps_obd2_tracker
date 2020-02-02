import logging
from . import api

logger = logging.getLogger(__name__)

class DeviceStatus:

    def __init__(self, interface):

        self.api = interface
    
    def get_device_status(self):

        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        json = self.api.getRequest("GetDeviceStatus", payload)
        logger.debug(json)
        self.api.doSave(json)

    def get_device_status2_by_DDC(self):
            
        payload = {
            "DeviceID": self.api.deviceID,
            "Language": self.api.language
        }
        json = self.api.getRequest("GetDeviceStatus2ByDDC", payload)
        logger.debug(json)
        self.api.doSave(json)
        
    def get_device_status_FZE(self):
        
        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        json = self.api.getRequest("GetDeviceStatusFZE", payload)
        logger.debug(json)
        self.api.doSave(json)