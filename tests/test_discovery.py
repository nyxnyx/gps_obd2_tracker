import pytest
from unittest.mock import patch, MagicMock
from obdtracker.discovery import get_app_address

@pytest.mark.asyncio
async def test_get_app_address_success():
    class MockResponse:
        def raise_for_status(self): pass
        @property
        def text(self): return "http://app.server.com "
        
    class MockClient:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, url):
            assert url == "http://testserver.com/getapp.aspx"
            return MockResponse()

    with patch('httpx.AsyncClient', return_value=MockClient()):
        result = await get_app_address("http://testserver.com")
        assert result == "http://app.server.com"

@pytest.mark.asyncio
async def test_get_app_address_default():
    class MockResponse:
        def raise_for_status(self): pass
        @property
        def text(self): return "http://default.server.com"
        
    class MockClient:
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, url):
            assert url == "http://www.aika168.com/getapp.aspx"
            return MockResponse()

    with patch('httpx.AsyncClient', return_value=MockClient()):
        result = await get_app_address("")
        assert result == "http://default.server.com"
