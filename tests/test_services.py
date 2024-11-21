from datetime import datetime
from unittest import mock

import pytest
from werkzeug.exceptions import NotFound

from app import create_app
from app.stocks.models import StockInformation, StockValues, PerformanceData
from app.stocks.services import create_stock, get_stock_by_company_code


@pytest.fixture
def app():
    return create_app("testing")


def test_create_stock_success():
    stock_values = StockValues(open=1.1, high=5, low=3, close=6)
    stock_info = StockInformation(
        status="ok",
        purchased_amount=0,
        purchased_status="",
        request_data=datetime.now().strftime("%Y-%m-%d"),
        company_code="AAPL",
        company_name="Apple Inc",
        stock_values=stock_values,
        performance_data=PerformanceData(**{}),
        competitors=[],
    )

    with mock.patch('app.stocks.services.db.session') as mock_session:
        mock_add = mock_session.add
        mock_commit = mock_session.commit
        mock_rollback = mock_session.rollback

        create_stock(stock_info)

        mock_add.assert_called_once_with(stock_info)
        mock_commit.assert_called_once()
        mock_rollback.assert_not_called()


def test_create_stock_failure():
    stock_values = StockValues(open=1.1, high=5, low=3, close=6)
    stock_info = StockInformation(
        status="ok",
        purchased_amount=0,
        purchased_status="",
        request_data=datetime.now().strftime("%Y-%m-%d"),
        company_code="AAPL",
        company_name="Apple Inc",
        stock_values=stock_values,
        performance_data=PerformanceData(**{}),
        competitors=[],
    )

    with mock.patch('app.stocks.services.db.session') as mock_session:
        mock_add = mock_session.add
        mock_commit = mock_session.commit
        mock_rollback = mock_session.rollback

        mock_commit.side_effect = Exception("Error on saving stock")

        with pytest.raises(Exception):
            create_stock(stock_info)

        mock_add.assert_called_once_with(stock_info)

        mock_commit.assert_called_once()
        mock_rollback.assert_called_once()


@pytest.fixture()
def test_get_stock_by_company_code_found(app):
    stock_symbol = "AAPL"

    mock_stock = mock.Mock(spec=StockInformation)
    mock_stock.company_code = stock_symbol
    mock_stock.name = "Apple Inc."

    with mock.patch.object(StockInformation.query, 'filter',
                           return_value=mock.Mock(first=mock.Mock(return_value=mock_stock))):
        with app.app_context():
            result = get_stock_by_company_code(stock_symbol)

            assert result == mock_stock
            assert result.company_code == stock_symbol


@pytest.fixture()
def test_get_stock_by_company_code_not_found(app):
    stock_symbol = "AAPL"

    with mock.patch.object(StockInformation.query, 'filter',
                           return_value=mock.Mock(first=mock.Mock(return_value=None))):
        with pytest.raises(NotFound, match=f"Stock symbol '{stock_symbol}' not found in the database."):
            with app.app_context():
                get_stock_by_company_code(stock_symbol)
