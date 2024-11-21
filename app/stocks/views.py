from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from app import cache
from app.stocks.schemas import StockInformationSchemaSchema
from app.stocks.services import update_stock, get_stock_data

stock_bp = Blueprint('stocks', __name__)


@stock_bp.route('/stocks/<stock_symbol>/<date>', methods=('GET',))
@cache.cached(timeout=60)
async def get_stock(stock_symbol, date):
    stock = await get_stock_data(stock_symbol, date)
    return StockInformationSchemaSchema().jsonify(stock), 200


@stock_bp.route('/stocks/<stock_symbol>', methods=('POST',))
def update_by_stock_symbol(stock_symbol):
    data = request.get_json()

    if not data or 'amount' not in data:
        raise BadRequest("Invalid input, amount is required")

    amount = data['amount']
    if not isinstance(amount, (int, float)):
        raise BadRequest("amount must be a number")

    update_stock(amount, stock_symbol)

    return jsonify({'message': f'{amount} units of stock {stock_symbol}', }), 201
