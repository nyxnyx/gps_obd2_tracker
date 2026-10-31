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
    mock_api.device_info = DeviceInfo(
        device_id=123, device_name="A", model=90, sn="17000000001"
    )
    mock_api.key = "session-key"

    result = await mock_api.send_command("DY")

    mock_api.get_request.assert_called_once_with("SendCommandByAPP", {
        "SN": "17000000001",
        "DeviceID": 123,
        "CommandType": "808DYD",
        "Model": 90,
        "Paramter": "",
        "Key": "session-key",
    })
    assert result == response_data

@pytest.mark.asyncio
async def test_api_send_command_passes_unknown_types_through(mock_api):
    response_data = {"status": "success"}
    mock_api.get_request.return_value = response_data
    mock_api.device_info = DeviceInfo(
        device_id=123, device_name="A", model=90, sn="17000000001"
    )
    mock_api.key = "session-key"

    await mock_api.send_command("808DYD")
    mock_api.get_request.assert_called_once_with("SendCommandByAPP", {
        "SN": "17000000001",
        "DeviceID": 123,
        "CommandType": "808DYD",
        "Model": 90,
        "Paramter": "",
        "Key": "session-key",
    })

@pytest.mark.asyncio
async def test_api_get_command_list(mock_api):
    response_data = {"commandArr": []}
    mock_api.get_request.return_value = response_data
    mock_api.device_info = DeviceInfo(
        device_id=123, device_name="A", model=90, sn="17000000001"
    )
    mock_api.key = "session-key"

    result = await mock_api.get_command_list(page_no=1, page_count=50)

    mock_api.get_request.assert_called_once_with("GetCommandList", {
        "SN": "17000000001",
        "DeviceID": 123,
        "PageNo": "1",
        "PageCount": "50",
        "TimeZones": "2:00",
        "Language": "en",
        "Key": "session-key",
    })
    assert result == response_data

@pytest.mark.asyncio
async def test_api_get_response(mock_api):
    response_data = {"isResponse": "1"}
    mock_api.get_request.return_value = response_data
    mock_api.device_info = DeviceInfo(
        device_id=123, device_name="A", model=90, sn="17000000001"
    )
    mock_api.key = "session-key"

    result = await mock_api.get_response(command_id=42)

    mock_api.get_request.assert_called_once_with("GetResponse", {
        "SN": "17000000001",
        "DeviceID": 123,
        "CommandID": "42",
        "TimeZones": "2:00",
        "Key": "session-key",
    })
    assert result == response_data
