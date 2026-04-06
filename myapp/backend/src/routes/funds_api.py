from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

funds_bp = Blueprint("funds_api", __name__)

class AddFundsAPI(MethodView):
    def post(self):
        data = request.get_json()

        user_id = data.get("user_id")
        amount = data.get("amount")

        if user_id is None or amount is None:
            return jsonify({"message": "Missing user_id or amount"}), 400

        db = get_db()
        cursor = db.cursor()

        query = "CALL AddFunds(%s, %s)"
        cursor.execute(query, (amount, user_id))
        db.commit()

        cursor.close()

        return jsonify({"message": "Funds added successfully"}), 200


funds_view = AddFundsAPI.as_view("funds_api")

funds_bp.add_url_rule(
    "/add-funds",
    view_func=funds_view,
    methods=["POST"]
)