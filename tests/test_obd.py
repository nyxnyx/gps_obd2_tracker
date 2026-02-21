import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from obdtracker.obd import OBD

@pytest.fixture
def api_mock():
    mock = AsyncMock()
    mock.deviceID = "123"
    mock.get_request = AsyncMock(return_value={"obd_data": "ok"})
    mock.update_from_response = MagicMock()
    return mock

@pytest.mark.asyncio
async def test_obd_get_obd_data(api_mock):
    updater = OBD(api_mock)
    await updater.get_obd_data()
    api_mock.get_request.assert_called_once_with("GetOBDCheck", {
        "DeviceID": "123"
    })
    api_mock.update_from_response.assert_called_once_with({"obd_data": "ok"})

@pytest.mark.asyncio
async def test_obd_update(api_mock):
    updater = OBD(api_mock)
    updater.get_obd_data = AsyncMock()
    await updater.update()
    updater.get_obd_data.assert_called_once()
