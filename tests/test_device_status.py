import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from obdtracker.device_status import DeviceStatus

@pytest.fixture
def api_mock():
    mock = AsyncMock()
    mock.deviceID = "123"
    mock.timeZone = "2:00"
    mock.language = "en"
    mock.get_request = AsyncMock(return_value={"status": "ok"})
    mock.update_from_response = MagicMock()
    return mock

@pytest.mark.asyncio
async def test_device_status_get_device_status(api_mock):
    updater = DeviceStatus(api_mock)
    await updater.get_device_status()
    api_mock.get_request.assert_called_once_with("GetDeviceStatus", {
        "DeviceID": "123", "TimeZones": "2:00", "Language": "en", "FilterWarn": ""
    })
    api_mock.update_from_response.assert_called_once_with({"status": "ok"})

@pytest.mark.asyncio
async def test_device_status_get_device_status2_by_ddc(api_mock):
    updater = DeviceStatus(api_mock)
    await updater.get_device_status2_by_ddc()
    api_mock.get_request.assert_called_once_with("GetDeviceStatus2ByDDC", {
        "DeviceID": "123", "Language": "en"
    })
    api_mock.update_from_response.assert_called_once_with({"status": "ok"})

@pytest.mark.asyncio
async def test_device_status_get_device_status_fze(api_mock):
    updater = DeviceStatus(api_mock)
    await updater.get_device_status_fze()
    api_mock.get_request.assert_called_once_with("GetDeviceStatusFZE", {
        "DeviceID": "123", "TimeZones": "2:00", "Language": "en", "FilterWarn": ""
    })
    api_mock.update_from_response.assert_called_once_with({"status": "ok"})

@pytest.mark.asyncio
async def test_device_status_update(api_mock):
    updater = DeviceStatus(api_mock)
    updater.get_device_status = AsyncMock()
    await updater.update()
    updater.get_device_status.assert_called_once()
