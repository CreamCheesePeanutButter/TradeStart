from flask import request, Blueprint, jsonify
from flask.views import MethodView
from flask import Flask, session, redirect, url_for, request
from db import get_db
from tracker.user import User
login_bp = Blueprint('login_api', __name__)

# user_data = None

class LoginAPI(MethodView):

    def post(self):
        global user_data

        data = request.get_json()
        password = data.get('password')
        identifier = data.get('identifier')  # email or username

        if not password or not identifier:
            return jsonify({"message": "Missing credentials"}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = """
        CALL ValidateLogin(%s, %s);
        """

        cursor.execute(query, (password, identifier))
        result = cursor.fetchone()
        print(result)

        cursor.close()

        if result:
            # user = User(result["userID"], result["last_name"], result["first_name"], result["invested_funds"], result["available_funds"])
            # session["test"] = user.to_dict()
            return jsonify({
                "user": {
                    "userID": result["userID"],
                    "username": result["username"],
                    "email": result["email"],
                    "available_funds": result["available_funds"]
                },
                "token": result["userID"]
            }), 200

        return jsonify({"message": "Invalid credentials"}), 401


user_view = LoginAPI.as_view('user_api')

login_bp.add_url_rule(
    '/login',
    view_func=user_view,
    methods=['POST']
)