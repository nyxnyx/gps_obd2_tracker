import logging
from . import api, updater

logger = logging.getLogger(__name__)

class Location(updater.isUpdater):

    def __init__(self, interface):

        self.api = interface

    def getTracking(self):

        payload = {
            "DeviceID": self.api.deviceID,
            "Model": self.api.model,
            "TimeZones": self.api.timeZone,
            "MapType": "Google",
            "Language": self.api.language
        }

        json = self.api.getRequest("GetTracking", payload)
        logger.debug(json)
        self.api.doSave(json)
    
    def update(self):
        self.getTracking()