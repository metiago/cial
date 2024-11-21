from unittest import mock

import pytest

from app import create_app
from app.stocks.helpers import fetch_data
from app.stocks.marketwatch import MARKETWATCH_URL


@pytest.fixture
def app():
    return create_app("testing")


@pytest.mark.asyncio
async def test_fetch_data_wrong_response_type():
    mock_response = mock.MagicMock()
    mock_response.status = 500

    with mock.patch("aiohttp.ClientSession.get", return_value=mock_response):
        with pytest.raises(Exception):
            await fetch_data(MARKETWATCH_URL, {}, '')


@pytest.mark.asyncio
async def test_fetch_data_text_success():
    mock_response = mock.MagicMock()
    mock_response.status = 200

    with mock.patch("aiohttp.ClientSession.get", return_value=mock_response):
        result = await fetch_data(MARKETWATCH_URL.format("AAPL"), {}, 'text')
        assert result is not None
