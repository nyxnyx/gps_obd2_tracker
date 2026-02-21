import logging
from .updater import BaseUpdater

logger = logging.getLogger(__name__)

class OBD(BaseUpdater):
    """Component to update OBD data from the API."""
    
    async def get_obd_data(self):
        """Fetch OBD status/data."""
        payload = {
            "DeviceID": self.api.deviceID
        }
        data = await self.api.get_request("GetOBDCheck", payload)
        logger.debug("OBD Data: %s", data)
        self.api.update_from_response(data)

    async def update(self):
        """Default update implementation."""
        await self.get_obd_data()
