import logging
from . import api, updater

logger = logging.getLogger(__name__)

class Location(updater.isUpdater):

    def __init__(self, interface):

        self.api = interface

    async def getTracking(self):

        payload = {
            "DeviceID": self.api.deviceID,
            "Model": self.api.model,
            "TimeZones": self.api.timeZone,
            "MapType": "Google",
            "Language": self.api.language
        }

        json = await self.api.getRequest("GetTracking", payload)
        logger.debug(json)
        self.api.doSave(json)
    
    async def update(self):
        await self.getTracking()