import pytest
from unittest.mock import AsyncMock, patch
from obdtracker.updater import BaseUpdater

def test_base_updater_init():
    api_mock = object()
    updater = BaseUpdater(api_mock)
    assert updater.api is api_mock

@pytest.mark.asyncio
async def test_base_updater_update_not_implemented():
    api_mock = object()
    updater = BaseUpdater(api_mock)
    with pytest.raises(NotImplementedError):
        await updater.update()
