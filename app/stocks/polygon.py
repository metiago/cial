from .helpers import fetch_data

POLYGON_URL = "https://api.polygon.io/v1/open-close/{}/{}"
POLYGON_HEADERS = {
    "Authorization": "Bearer bmN7i7CrzrpKqFvgbB1fEaztCwZKSUjJ"
}


async def fetch_polygon_api(stock_symbol, date):
    return await fetch_data(POLYGON_URL.format(stock_symbol, date), POLYGON_HEADERS, "json")
