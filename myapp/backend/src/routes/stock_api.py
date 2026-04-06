# I would use the Massive api to get the data when we show the TA but for the testing data i would use OpenAPI data as it is unlimited

# As you can see I copy the exact same lib for this 
from datetime import datetime, timedelta
from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db
from tracker.stock_tracker import StockTracker

# The blueprint now is stock_api
stock_bp = Blueprint('stock_api', __name__)

# Single shared instance — both views must use the same tracker
# so that exchange_currency changes are visible to the GET endpoint
_tracker = StockTracker()


class StockAPI(MethodView):
    def get(self):
        # For now we just return the data in the stock tracker
        # In the future we can add more features like adding new stocks to track, etc.
        # update stock data to the SQL database

        db = get_db()         # connection
        cursor = db.cursor()  # cursor object
        # check if the last called time is more than 1 minute ago, if so, update the stock data
        cursor.execute("SELECT last_call FROM stock LIMIT 1")
        result = cursor.fetchone()
        if result is None or (result[0] is None) or (result[0] < (datetime.now() - timedelta(minutes=1))):
            for ticker, stock in _tracker.get_stocks().items():
                cursor.execute(
                    """
                    CALL UpdateStocks(%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (ticker, stock.current_price, stock.high_today, stock.low_today, stock.open_price, stock.previous_close, stock.name, stock.currency)
                )
            db.commit()
            cursor.close()
        return jsonify({
            "stocks": {
                ticker: {
                    "stock_key" : ticker,
                    "name" :  stock.name,
                    "current_price": stock.current_price,
                    "high_today": stock.high_today,
                    "low_today": stock.low_today,
                    "open_price": stock.open_price,
                    "previous_close": stock.previous_close,
                } for ticker, stock in _tracker.get_stocks().items()},
            "currency": _tracker.get_currency()

        }), 200  

user_view = StockAPI.as_view('user_api')
stock_bp.add_url_rule('/stocks', view_func=user_view, methods=['GET'])

class StockExchangeCurrencyAPI(MethodView):
    def post(self):
        currency = ""
        if _tracker.get_currency() == "CAD":
            _tracker.exchange_currency("USD")
            currency = "USD"
        else:
            _tracker.exchange_currency("CAD")
            currency = "CAD"
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE stock SET currency = %s", (currency,))
        db.commit()
        cursor.close()

        return jsonify({
            "stocks": {
                ticker: {
                    "stock_key" : ticker,
                    "name" :  stock.name,
                    "current_price": stock.current_price,
                    "high_today": stock.high_today,
                    "low_today": stock.low_today,
                    "open_price": stock.open_price,
                    "previous_close": stock.previous_close,
                } for ticker, stock in _tracker.get_stocks().items()},
            "message": f"Exchange rate updated to {currency}",
            "currency": currency,

        }), 200
    
stock_bp.add_url_rule('/stocks/exchange', view_func=StockExchangeCurrencyAPI.as_view('stock_exchange'), methods=['POST'])