import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__=['login_action', 'device_status', 'obd', 'location']

APP_ENDPOINT="/getapp.aspx"

def getapp(server) -> str:
    """
    Returns application address from server. 
    If server address is an empty string will use http://www.aika168.com
    """

    if server == "":
        server = "http://www.aika168.com"
        
    r = requests.get(server+APP_ENDPOINT)
    logger.debug(r.content)
    return ""+str(r.content.decode())
    