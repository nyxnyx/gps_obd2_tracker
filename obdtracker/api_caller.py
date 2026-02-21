import httpx
import logging
import asyncio
import xml.etree.ElementTree
from typing import Optional, Dict, Any
from . import utils
from .discovery import get_app_address
from .exceptions import ObdTrackerConnectionError, ObdTrackerParseError

logger = logging.getLogger(__name__)

DEFAULT_HEADER = {'Content-Type': 'application/x-www-form-urlencoded'}

class ApiCaller:
    """
    Base class for all requests to API. 
    Handles network communication and basic response parsing.
    """
    
    def __init__(self, server: str):
        self.api_source = server
        self.api_address: str = "" 
        self.key: Optional[str] = None
        self.device_id: Optional[str] = None
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        """Initialize the API address and client."""
        if not self.api_address:
            self.api_address = await get_app_address(self.api_source)
        
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=30.0)
        logger.debug("Connected to %s", self.api_address)

    async def close(self):
        """Close the underlying HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _add_key(self, request_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Add session key to payload if required."""
        if request_name != 'Login' and "Key" not in payload:
            payload["Key"] = self.key
        return payload

    async def get_request(self, request_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs an API request and returns the parsed JSON response.
        """
        if self._client is None:
            await self.connect()

        request_name = request_name.strip('/')
        self._add_key(request_name, payload)
        
        if self.device_id is None and "DeviceID" in payload:
            self.device_id = str(payload["DeviceID"])

        logger.debug("Request: %s/%s | Payload: %s", self.api_address, request_name, payload)

        try:
            response = await self._client.post(
                f"{self.api_address}/{request_name}",
                data=payload,
                headers=DEFAULT_HEADER
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise ObdTrackerConnectionError(f"HTTP request failed: {e}") from e

        try:
            # The API returns JSON wrapped in XML text
            data = utils.getJSON(response.text)
        except Exception as e:
            logger.debug("Raw response: %s", response.text)
            raise ObdTrackerParseError(f"Failed to parse API response: {e}") from e

        if request_name == "Login" and "deviceInfo" in data:
            self.key = data["deviceInfo"].get("key2018")

        return data

    async def logout(self):
        """Signal the API that we are exiting."""
        if self.device_id and self.key:
            try:
                await self.get_request(
                    "ExitAndroid", 
                    payload={"ID": self.device_id, "TypeID": "1", "Key": self.key}
                )
            except Exception:
                pass # Best effort logout

