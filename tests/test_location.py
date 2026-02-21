import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from obdtracker.location import Location

@pytest.fixture
def api_mock():
    mock = AsyncMock()
    mock.deviceID = "123"
    mock.model = 456
    mock.timeZone = "2:00"
    mock.language = "en"
    mock.get_request = AsyncMock(return_value={"lat": "1.0"})
    mock.update_from_response = MagicMock()
    return mock

@pytest.mark.asyncio
async def test_location_get_tracking(api_mock):
    updater = Location(api_mock)
    await updater.get_tracking()
    api_mock.get_request.assert_called_once_with("GetTracking", {
        "DeviceID": "123", "Model": 456, "TimeZones": "2:00", "MapType": "Google", "Language": "en"
    })
    api_mock.update_from_response.assert_called_once_with({"lat": "1.0"})

@pytest.mark.asyncio
async def test_location_update(api_mock):
    updater = Location(api_mock)
    updater.get_tracking = AsyncMock()
    await updater.update()
    updater.get_tracking.assert_called_once()
