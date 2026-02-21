import logging
from typing import List, Optional, Any
from . import api_caller
from .updater import BaseUpdater
from .models import DeviceInfo, LocationData, DeviceStatusData

logger = logging.getLogger(__name__)

APP_KEY = '7DU2DJFDR8321'

class API(api_caller.ApiCaller):
    """
    Main API class to interact with the OBD2 Tracker service.
    """
    
    def __init__(self, server: str):
        super().__init__(server)
        self.language = "en"
        self.updaters: List[BaseUpdater] = []
        
        # Data storage
        self.device_info: Optional[DeviceInfo] = None
        self.location: Optional[LocationData] = None
        self.status: Optional[DeviceStatusData] = None

    async def login(self, username, password):
        """Perform login and store device information."""
        payload = {
            'Name': username,
            'Pass': password,
            'LoginType': 1,
            'LoginAPP': "AKSH",
            'GMT': "2:00",
            'Key': APP_KEY
        }

        data = await self.get_request('Login', payload)
        logger.debug("Login response: %s", data)
        
        if "deviceInfo" in data:
            self.device_info = DeviceInfo.from_dict(data["deviceInfo"])
            # Backward compatibility for IDs if needed
            self.device_id = str(self.device_info.device_id)
            
    def update_from_response(self, response_data: dict):
        """Update internal state from an API response dictionary."""
        # This is a generic way to update if the response contains multiple bits of info
        if "deviceInfo" in response_data:
            self.device_info = DeviceInfo.from_dict(response_data["deviceInfo"])
        
        # Check for location-like data
        if any(k in response_data for k in ["lat", "lng", "speed"]):
            self.location = LocationData.from_dict(response_data)
            
        # Check for status-like data
        if any(k in response_data for k in ["battery", "batteryStatus", "xg"]):
            self.status = DeviceStatusData.from_dict(response_data)

    async def send_command(self, content: str):
        """
        Send a generic command via the platform.
        This sends a command that gets forwarded to the device (similar to SMS).
        """
        payload = {
            "DeviceID": self.device_id,
            "Content": content
        }
        data = await self.get_request("SendCommand", payload)
        logger.debug("Send command response: %s", data)
        return data

    async def update(self):
        """Execute all registered updaters."""
        for updater in self.updaters:
            await updater.update()

    def register_updater(self, updater_instance: BaseUpdater):
        """Register a new updater component."""
        if isinstance(updater_instance, BaseUpdater):
            self.updaters.append(updater_instance)

    # Legacy method names for compatibility if needed, but we should encourage new ones
    async def doLogin(self, username, password): return await self.login(username, password)
    async def doUpdate(self): return await self.update()
    def registerUpdater(self, interface): return self.register_updater(interface)
    def doSave(self, response): return self.update_from_response(response)

    @property
    def deviceID(self): return self.device_info.device_id if self.device_info else None
    @property
    def model(self): return self.device_info.model if self.device_info else None
    @property
    def timeZone(self): return "2:00" # Default from payload, could be made dynamic