import asyncio
from unittest.mock import patch

import pytest

from app import create_app


@pytest.fixture
def app():
    return create_app("testing")


@pytest.mark.asyncio
async def test_get_stock_not_found(app):
    stock_symbol = 'OOTC'
    date = '2023-10-01'
    expected = {'code': 404,
                'message': '404 Not Found: Resource not found (404) for URL: https://api.polygon.io/v1/open-close/OOTC/2023-10-01'}
    with patch('app.stocks.views.get_stock') as mock_resp:
        mock_resp.return_value = {'symbol': stock_symbol, 'date': date, 'price': 150.0}

        def sync_test():  # workaround provided by the community to handle async tests
            with app.test_client() as client:
                response = client.get(f'/stocks/{stock_symbol}/{date}')
                assert response.status_code == 404
                assert expected == response.json

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_test)


@pytest.mark.asyncio
async def test_get_stock_ok(app):
    stock_symbol = 'AAPL'
    date = '2023-04-20'
    with patch('app.stocks.views.get_stock') as mock_resp:
        mock_resp.return_value = {'symbol': stock_symbol, 'date': date, 'price': 150.0}

        def sync_test():
            with app.test_client() as client:
                response = client.get(f'/stocks/{stock_symbol}/{date}')
                assert response.status_code == 200

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_test)


@pytest.mark.asyncio
async def test_update_stock_ok(app):
    amount = "1.99"
    stock_symbol = "AAPL"
    payload = {"amount": 1.99}
    success_message = {"message": f"{amount} units of stock {stock_symbol}"}
    with patch('app.stocks.views.update_by_stock_symbol') as mock_resp:
        mock_resp.return_value = success_message

        def sync_test():
            with app.test_client() as client:
                response = client.post(f'/stocks/{stock_symbol}', json=payload)
                assert response.status_code == 201
                assert response.json == success_message

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_test)


@pytest.mark.asyncio
async def test_update_stock_valid_amount_required(app):
    error_message = {
        "code": 400,
        "message": "400 Bad Request: Invalid input, amount is required"
    }
    stock_symbol = "AAPL"
    payload = {"total": 1.99}
    with patch('app.stocks.views.update_by_stock_symbol') as mock_resp:
        mock_resp.return_value = error_message

        def sync_test():
            with app.test_client() as client:
                response = client.post(f'/stocks/{stock_symbol}', json=payload)
                assert response.status_code == 400
                assert response.json == error_message

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_test)


@pytest.mark.asyncio
async def test_update_stock_invalid_amount_type(app):
    error_message = {
        "code": 400,
        "message": "400 Bad Request: amount must be a number"
    }
    stock_symbol = "AAPL"
    payload = {"amount": "233"}
    with patch('app.stocks.views.update_by_stock_symbol') as mock_resp:
        mock_resp.return_value = error_message

        def sync_test():
            with app.test_client() as client:
                response = client.post(f'/stocks/{stock_symbol}', json=payload)
                assert response.status_code == 400
                assert response.json == error_message

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, sync_test)
