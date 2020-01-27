import logging
import requests

from . import login_action, utils

logger = logging.getLogger(__name__)


class OBD:

    def __init__(self, loginAction):
        
        if loginAction.getKey2018() == "":
            logger.error("No Key2018!!! Did you log in?")
        else:
            self._la = loginAction
    
    def get_obd_data(self):

        payload = {
            "DeviceID": self._la._deviceID,
            "Key": self._la._key2018
        }
        r = requests.get(self._la.getAddress() + "/GetOBDCheck",
                params = payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
        json = utils.getJSON(r.content.decode())
        logger.debug(json)
