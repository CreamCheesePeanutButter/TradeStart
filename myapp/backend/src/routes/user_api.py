from flask import request, Blueprint, jsonify, session
from flask.views import MethodView
from db import get_db
from tracker.user import User
from datetime import datetime, timedelta

user_bp = Blueprint('user_api', __name__)

class UserAPI(MethodView):

        def get(self, user_id):
            db = get_db()

            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM user WHERE userID = %s", (user_id,))

            users = cursor.fetchall() #store all user data
            cursor.close()
            print(users)
            return jsonify({
                "users": [
                    {
                        "id": user['userID'],
                        "email": user['email'],
                        "first_name": user['first_name'],
                        "last_name": user['last_name'],
                        "username": user['username'],
                        "available_funds": user['available_funds']
                    } for user in users
                ]
            }), 200

user_view = UserAPI.as_view('user_api')
# this piece of code is for getting user information.

user_bp.add_url_rule(
    '/user/<int:user_id>/info',
    view_func=user_view,
    methods=['GET']
)
### Example of the what the API will return
# {
#   "users": [
#     {
#       "available_funds": 0.0,
#       "email": "jdoe@example.com",
#       "first_name": "John",
#       "id": 1,
#       "last_name": "Doe",
#       "username": "jdoe"
#     }
#   ]
# }
####

#####################ADD FUNDS API#####################
class UserFundsAPI(MethodView):

    def post(self, user_id):
        data = request.get_json()
        amount = data.get('amount')

        if amount is None:
            return jsonify({"message": "Missing amount"}), 400

        db = get_db()
        cursor = db.cursor()

        cursor.execute("UPDATE user SET available_funds = available_funds + %s WHERE userID = %s", (amount, user_id))
        db.commit()
        cursor.close()

        return jsonify({"message": "Funds added successfully"}), 200
    
user_funds_view = UserFundsAPI.as_view('user_funds_api')
user_bp.add_url_rule(
    '/user/<int:user_id>/add-funds',
    view_func=user_funds_view,
    methods=['POST']
)

###########################Buy stock 

from tracker.stock_tracker import StockTracker
_stockTracker = StockTracker()
def update_stocks():
    db = get_db()         # connection
    cursor = db.cursor()  # cursor object
    # check if the last called time is more than 1 minute ago, if so, update the stock data
    cursor.execute("SELECT last_call FROM stock LIMIT 1")
    result = cursor.fetchone()
    if result is None or (result[0] is None) or (result[0] < (datetime.now() - timedelta(minutes=1))):
        for ticker, stock in _stockTracker.get_stocks().items():
            cursor.execute(
                """
                CALL UpdateStocks(%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (ticker, stock.current_price, stock.high_today, stock.low_today, stock.open_price, stock.previous_close, stock.name, stock.currency)
            )
        db.commit()
        cursor.close()
class BuyAPI(MethodView):

    def post(self, user_id):
        update_stocks()
        data = request.get_json()

        num_share = data.get("num_share")
        stock_key = data.get("stock_key")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # get user
        cursor.execute(
            "SELECT * FROM user WHERE userID = %s",
            (user_id,)
        )

        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({"message": "User not found"}), 404

        # get stock price
        cursor.execute(
            "SELECT current_price FROM stock WHERE stock_key = %s",
            (stock_key,)
        )

        stock = cursor.fetchone()

        if not stock:
            return jsonify({"message": "Stock not found"}), 404

        price = float(stock["current_price"])

        user = User.from_dict(user_data)

        success = user.buy(num_share, price, stock_key)

        if not success:
            return jsonify({"message": "Not enough funds"}), 400

        return jsonify({
            "message": "BUY successful",
            "price": price,
            "shares": num_share
        }), 200


class SellAPI(MethodView):

    def post(self, user_id):
        update_stocks()
        data = request.get_json()

        num_share = data.get("num_share")
        stock_key = data.get("stock_key")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # get user
        cursor.execute(
            "SELECT * FROM user WHERE userID = %s",
            (user_id,)
        )

        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({"message": "User not found"}), 404

        # get price
        cursor.execute(
            "SELECT current_price FROM stock WHERE stock_key = %s",
            (stock_key,)
        )

        stock = cursor.fetchone()

        if not stock:
            return jsonify({"message": "Stock not found"}), 404

        price = float(stock["current_price"])

        user = User.from_dict(user_data)

        success = user.sell(num_share, price, stock_key)

        if not success:
            return jsonify({"message": "Not enough shares"}), 400

        return jsonify({
            "message": "SELL successful",
            "price": price,
            "shares": num_share
        }), 200
    
buy_view = BuyAPI.as_view("buy_api")
sell_view = SellAPI.as_view("sell_api")

user_bp.add_url_rule(
    "/user/<int:user_id>/buy",
    view_func=buy_view,
    methods=["POST"]
)

user_bp.add_url_rule(
    "/user/<int:user_id>/sell",
    view_func=sell_view,
    methods=["POST"]
)

###########################Portfolio API

class PortfolioAPI(MethodView):

    def get(self, user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            CALL GetPortfolio(%s)
            """,
            (user_id,)
        )

        holdings = cursor.fetchall()
        cursor.close()

        return jsonify({
            "portfolio": [
                {
                    "symbol": h["stock_symbol"],
                    "companyName": h["name"] or h["stock_symbol"],
                    "shares": int(h["total_shares"]),
                    "avgPrice": float(h["avg_price"] or 0),
                    "currentPrice": float(h["current_price"] or 0),
                }
                for h in holdings
            ]
        }), 200

portfolio_view = PortfolioAPI.as_view("portfolio_api")
user_bp.add_url_rule(
    "/user/<int:user_id>/portfolio",
    view_func=portfolio_view,
    methods=["GET"]
)

###########################Trade History API

class TradeHistoryAPI(MethodView):

    def get(self, user_id):
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            """
            CALL GetTradeHistory(%s)
            """,
            (user_id,)
        )

        rows = cursor.fetchall()
        cursor.close()

        return jsonify({
            "history": [
                {
                    "symbol": r["stock_symbol"],
                    "shares": abs(int(r["number_of_shares"])),
                    "price": float(r["price"]),
                    "total": float(r["price"]) * abs(int(r["number_of_shares"])),
                    "type": r["transaction_type"],
                    "date": r["transaction_date"].strftime("%Y-%m-%d %H:%M"),
                }
                for r in rows
            ]
        }), 200

history_view = TradeHistoryAPI.as_view("trade_history_api")
user_bp.add_url_rule(
    "/user/<int:user_id>/history",
    view_func=history_view,
    methods=["GET"]
)
