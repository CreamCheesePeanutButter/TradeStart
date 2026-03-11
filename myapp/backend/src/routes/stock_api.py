# I would use the Massive api to get the data when we show the TA but for the testing data i would use OpenAPI data as it is unlimited

# As you can see I copy the exact same lib for this 
from datetime import datetime, timedelta

from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db
from tracker.stock_tracker import StockTracker

# The blueprint now is stock_api
stock_bp = Blueprint('stock_api', __name__)

class StockAPI(MethodView):
    # We need GET API for allowing the frontend to get the stock data
    stock_tracker = StockTracker()
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
            for ticker, stock in self.stock_tracker.stocks.items():
                cursor.execute(
                    """
                    INSERT INTO stock (stock_key, current_price, high_price, low_price, open_price, previous_close)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        current_price = VALUES(current_price),
                        high_price = VALUES(high_price),
                        low_price = VALUES(low_price),
                        open_price = VALUES(open_price),
                        previous_close = VALUES(previous_close)
                    """,
                    (ticker, stock.current_price, stock.high_today, stock.low_today, stock.open_price, stock.previous_close)
                )
            db.commit()
            cursor.close()
        return jsonify({
            "stocks": {ticker: {
                "current_price": stock.current_price,
                "high_today": stock.high_today,
                "low_today": stock.low_today,
                "open_price": stock.open_price,
                "previous_close": stock.previous_close
            } for ticker, stock in self.stock_tracker.stocks.items()}
        })   

user_view = StockAPI.as_view('user_api')
stock_bp.add_url_rule('/stocks', view_func=user_view, methods=['GET'])