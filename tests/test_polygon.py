from datetime import datetime
from unittest import mock

import pytest

from app import create_app
from app.stocks.helpers import fetch_data
from app.stocks.polygon import POLYGON_URL


@pytest.fixture
def app():
    return create_app("testing")


@pytest.mark.asyncio
@pytest.mark.parametrize("stock_symbol", ["OOTC", "XNAS", "XNYS"])
async def test_multiples_fetch_data_json_success(stock_symbol):
    mock_response = mock.MagicMock()
    mock_response.status = 200
    mock_response.json = mock.AsyncMock(return_value={"key": "value"})

    with mock.patch("aiohttp.ClientSession.get", return_value=mock_response):
        result = await fetch_data(POLYGON_URL.format(stock_symbol, datetime.now()), {}, 'json')
        assert result is not None
