import asyncio
import logging
from datetime import datetime
from decimal import Decimal

from bs4 import BeautifulSoup
from werkzeug.exceptions import NotFound

from app import db
from .marketwatch import scrap_performance_data, scrap_competitors_data, fetch_marketwatch_webpage
from .models import StockInformation
from .models import StockValues
from .polygon import fetch_polygon_api


async def get_stock_data(stock_symbol, date):
    logging.info(f"Getting stock for stock symbol '{stock_symbol}' and date '{date}'")
    marketwatch, polygon = await asyncio.gather(fetch_marketwatch_webpage(stock_symbol),
                                                fetch_polygon_api(stock_symbol.upper(), date))

    soup = BeautifulSoup(marketwatch, 'html.parser')
    company_name_h1 = soup.find('h1', class_='company__name')

    performances = scrap_performance_data(soup)

    competitors = scrap_competitors_data(soup)

    stock_values = StockValues(open=polygon.get("open", None),
                               high=polygon.get("high", None),
                               low=polygon.get("low", None),
                               close=polygon.get("close", None))

    request_data = datetime.strptime(polygon.get("from"), "%Y-%m-%d") if polygon.get("from") else None
    stock_info = StockInformation(
        status=polygon.get("status", None),
        purchased_amount=0,
        purchased_status="",
        request_data=request_data,
        company_code=polygon.get("symbol", None),
        company_name=company_name_h1.text if company_name_h1 else None,
        stock_values=stock_values,
        performance_data=performances,
        competitors=competitors,
    )

    create_stock(stock_info)

    return stock_info


def create_stock(stock_info):
    try:
        logging.info(f"Creating stock '{stock_info}'")
        db.session.add(stock_info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(str(e))
        raise e


def update_stock(amount, stock_symbol):
    try:
        logging.info(f"Updating stock amount {amount} and symbol f{stock_symbol}")
        existing_stock = get_stock_by_company_code(stock_symbol)
        existing_stock.purchased_amount = Decimal(amount)
        existing_stock.purchased_status = "purchased"
        db.session.add(existing_stock)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(str(e))
        raise e


def get_stock_by_company_code(stock_symbol):
    logging.info(f"Initiating lookup for stock symbol '{stock_symbol}'")
    stock = StockInformation.query.filter(getattr(StockInformation, "company_code") == stock_symbol).first()
    if not stock:
        raise NotFound(f"Stock symbol '{stock_symbol}' not found in the database.")
    return stock
