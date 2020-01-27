import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__=['login_action', 'device_status', 'obd', 'location']

APP_ENDPOINT="/getapp.aspx"
APP_KEY = '7DU2DJFDR8321'

def getapp(host) -> str:
    '''Returns application address from host: host. 
    If host is an empty string will use http://www.aika168.com'''
    if host == "":
        host = "http://www.aika168.com"
    r = requests.get(host+APP_ENDPOINT)
    logger.debug(r.content)
    return ""+str(r.content.decode())
    