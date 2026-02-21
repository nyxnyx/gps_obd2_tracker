import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from obdtracker.api_caller import ApiCaller
from obdtracker.exceptions import ObdTrackerConnectionError, ObdTrackerParseError
import httpx

@pytest.mark.asyncio
async def test_apicaller_connect_close():
    with patch('obdtracker.api_caller.get_app_address', new_callable=AsyncMock) as mock_get_app:
        mock_get_app.return_value = "http://app.server"
        caller = ApiCaller("http://server")
        await caller.connect()
        assert caller.api_address == "http://app.server"
        assert caller._client is not None
        await caller.close()
        assert caller._client is None

@pytest.mark.asyncio
async def test_apicaller_context_manager():
    with patch('obdtracker.api_caller.get_app_address', new_callable=AsyncMock) as mock_get_app:
        mock_get_app.return_value = "http://app.server"
        async with ApiCaller("http://server") as caller:
            assert caller.api_address == "http://app.server"
            assert caller._client is not None
        assert caller._client is None

@pytest.mark.asyncio
async def test_apicaller_get_request_success():
    expected_response = {"deviceInfo": {"key2018": "testkey"}}
    
    mock_post = AsyncMock()
    mock_response = MagicMock()
    mock_response.text = "DummyXML"
    mock_post.return_value = mock_response

    with patch('obdtracker.api_caller.get_app_address', new_callable=AsyncMock, return_value="http://app.server"), \
         patch('httpx.AsyncClient.post', new=mock_post), \
         patch('obdtracker.utils.getJSON', return_value=expected_response):
        
        async with ApiCaller("http://server") as caller:
            result = await caller.get_request("Login", {"DeviceID": "123"})
            
            assert result == expected_response
            assert caller.device_id == "123"
            assert caller.key == "testkey"

@pytest.mark.asyncio
async def test_apicaller_get_request_add_key():
    expected_response = {"data": "test"}
    mock_post = AsyncMock()
    mock_response = MagicMock()
    mock_response.text = "DummyXML"
    mock_post.return_value = mock_response

    with patch('obdtracker.api_caller.get_app_address', new_callable=AsyncMock, return_value="http://app.server"), \
         patch('httpx.AsyncClient.post', new=mock_post), \
         patch('obdtracker.utils.getJSON', return_value=expected_response):
        
        async with ApiCaller("http://server") as caller:
            caller.key = "mykey"
            result = await caller.get_request("SomeAction", {})
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            assert kwargs["data"]["Key"] == "mykey"

@pytest.mark.asyncio
async def test_apicaller_http_error():
    mock_post = AsyncMock()
    mock_post.side_effect = httpx.HTTPError("Error")

    with patch('obdtracker.api_caller.get_app_address', new_callable=AsyncMock, return_value="http://app.server"), \
         patch('httpx.AsyncClient.post', new=mock_post):
        async with ApiCaller("http://server") as caller:
            with pytest.raises(ObdTrackerConnectionError):
                await caller.get_request("Action", {})
