from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

admin_bp = Blueprint("admin_api", __name__)
class AdminAPI(MethodView):
    def get(self):
        db = get_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()

        users = []

        for r in rows:
            users.append({
                "userID": r[0],
                "username": r[1],
                "password": r[2],
                "email": r[3],
                "first_name": r[4],
                "last_name": r[5],
                "admin_access": r[6],
                "available_funds": float(r[7]),
                "portfolio_value": float(r[8])
            })

        return jsonify(users)

    def put(self):  
        data = request.get_json()
        user_id = data.get("user_id")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE user SET admin_access = 1 WHERE userID = %s",
            (user_id,)
        )
        db.commit()

        return jsonify({"message": "User updated successfully"})

    def delete(self):
        data = request.get_json()
        user_id = data.get("user_id")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "DELETE FROM user WHERE userID = %s",
            (user_id,)
        )
        db.commit()

        return jsonify({"message": "User deleted successfully"})
    
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")


        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (username, password, first_name, last_name, admin_access) VALUES (%s, %s, %s, %s, 0)",
            (username, password, first_name, last_name)
        )
        db.commit()

        return jsonify({"message": "User created successfully"})

admin_bp.add_url_rule(
    "/admin/users",
    view_func=AdminAPI.as_view("admin_users_api")
)
class AdminTransactionAPI(MethodView):
    def get(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM TradeTable")
        transactions = cursor.fetchall()
    
        result = []
        for transaction in transactions:
            result.append({
                "tradeID": transaction[0],
                "userID": transaction[1],
                "stockSymbol": transaction[2],
                "quantity": transaction[3],
                "price": transaction[4],
                "timestamp": transaction[5].isoformat(),
                "tradeType": transaction[6]
            })
        return jsonify(result)

admin_bp.add_url_rule(
    "/admin/transactions",
    view_func=AdminTransactionAPI.as_view("admin_transactions_api")
)