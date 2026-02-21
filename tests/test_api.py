import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from obdtracker.api import API
from obdtracker.models import DeviceInfo, LocationData, DeviceStatusData
from obdtracker.updater import BaseUpdater

@pytest.fixture
def mock_api():
    api = API("http://server")
    api.get_request = AsyncMock()
    return api

@pytest.mark.asyncio
async def test_api_login(mock_api):
    response_data = {"deviceInfo": {"deviceID": "123", "deviceName": "A"}}
    mock_api.get_request.return_value = response_data
    
    await mock_api.login("user", "pass")
    
    mock_api.get_request.assert_called_once_with('Login', {
        'Name': 'user',
        'Pass': 'pass',
        'LoginType': 1,
        'LoginAPP': 'AKSH',
        'GMT': '2:00',
        'Key': '7DU2DJFDR8321'
    })
    
    assert mock_api.device_info is not None
    assert mock_api.device_info.device_id == 123
    assert mock_api.device_id == "123"

def test_update_from_response(mock_api):
    response = {
        "deviceInfo": {"deviceID": "999"},
        "lat": "1.0", "lng": "2.0", "speed": "0", "course": "0",
        "battery": "50", "batteryStatus": "Charge", "xg": "3"
    }
    
    mock_api.update_from_response(response)
    
    assert mock_api.device_info is not None
    assert mock_api.device_info.device_id == 999
    
    assert mock_api.location is not None
    assert mock_api.location.lat == 1.0
    
    assert mock_api.status is not None
    assert mock_api.status.battery == 50

@pytest.mark.asyncio
async def test_api_update(mock_api):
    mock_updater = MagicMock(spec=BaseUpdater)
    mock_updater.update = AsyncMock()
    
    mock_api.register_updater(mock_updater)
    await mock_api.update()
    
    mock_updater.update.assert_called_once()

@pytest.mark.asyncio
async def test_api_send_command(mock_api):
    response_data = {"status": "success"}
    mock_api.get_request.return_value = response_data
    mock_api.device_id = "123"
    
    result = await mock_api.send_command("DY")
    
    mock_api.get_request.assert_called_once_with("SendCommand", {
        "DeviceID": "123",
        "Content": "DY"
    })
    assert result == response_data
