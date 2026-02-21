import logging
from .updater import BaseUpdater

logger = logging.getLogger(__name__)

class DeviceStatus(BaseUpdater):
    """Component to update device status from the API."""

    async def get_device_status(self):
        """Fetch standard device status."""
        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        data = await self.api.get_request("GetDeviceStatus", payload)
        logger.debug("Device Status: %s", data)
        self.api.update_from_response(data)

    async def get_device_status2_by_ddc(self):
        """Fetch device status using DDC method."""
        payload = {
            "DeviceID": self.api.deviceID,
            "Language": self.api.language
        }
        data = await self.api.get_request("GetDeviceStatus2ByDDC", payload)
        logger.debug("Device Status DDC: %s", data)
        self.api.update_from_response(data)
        
    async def get_device_status_fze(self):
        """Fetch device status using FZE method."""
        payload = {
            "DeviceID": self.api.deviceID,
            "TimeZones": self.api.timeZone,
            "Language": self.api.language,
            "FilterWarn": ""
        }
        data = await self.api.get_request("GetDeviceStatusFZE", payload)
        logger.debug("Device Status FZE: %s", data)
        self.api.update_from_response(data)
    
    async def update(self):
        """Default update implementation."""
        await self.get_device_status()