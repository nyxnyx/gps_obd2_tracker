import logging
from .updater import BaseUpdater

logger = logging.getLogger(__name__)

class Location(BaseUpdater):
    """Component to update device location from the API."""

    async def get_tracking(self):
        """Fetch tracking data (GPS location)."""
        payload = {
            "DeviceID": self.api.deviceID,
            "Model": self.api.model,
            "TimeZones": self.api.timeZone,
            "MapType": "Google",
            "Language": self.api.language
        }

        data = await self.api.get_request("GetTracking", payload)
        logger.debug("Location Data: %s", data)
        self.api.update_from_response(data)
    
    async def update(self):
        """Default update implementation."""
        await self.get_tracking()