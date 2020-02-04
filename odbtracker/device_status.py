import logging
from . import api, updater

logger = logging.getLogger(__name__)

class DeviceStatus(updater.isUpdater):

    def __init__(self, interface):

        self.api = interface
    
    async def get_device_status(self):

        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        json = await self.api.getRequest("GetDeviceStatus", payload)
        logger.debug(json)
        self.api.doSave(json)

    async def get_device_status2_by_DDC(self):
            
        payload = {
            "DeviceID": self.api.deviceID,
            "Language": self.api.language
        }
        json = await self.api.getRequest("GetDeviceStatus2ByDDC", payload)
        logger.debug(json)
        self.api.doSave(json)
        
    async def get_device_status_FZE(self):
        
        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        json = await self.api.getRequest("GetDeviceStatusFZE", payload)
        logger.debug(json)
        self.api.doSave(json)
    
    async def update(self):
        await self.get_device_status()