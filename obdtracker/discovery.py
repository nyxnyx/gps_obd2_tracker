import httpx
import logging

logger = logging.getLogger(__name__)

APP_ENDPOINT = "/getapp.aspx"

async def get_app_address(server: str) -> str:
    """
    Returns application address from server. 
    If server address is an empty string will use http://www.aika168.com
    """
    if not server:
        server = "http://www.aika168.com"
        
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(server + APP_ENDPOINT)
            r.raise_for_status()
            address = r.text.strip()
            logger.debug("App address: %s", address)
            return address
        except httpx.HTTPError as e:
            logger.error("Failed to get app address: %s", e)
            return ""
