import logging
import requests

from . import api, utils

logger = logging.getLogger(__name__)


class OBD:

    def __init__(self, interface):
        
        self.api = interface
    
    def get_obd_data(self):

        payload = {
            "DeviceID": self.api.deviceID
        }
        json = self.api.getRequest("GetOBDCheck", payload)
        logger.debug(json)
        self.api.doSave(payload)
