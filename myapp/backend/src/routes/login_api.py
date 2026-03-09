from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

login_bp = Blueprint('login_api', __name__)

class LoginAPI(MethodView):

    def post(self):
        data = request.get_json()
        password = data.get('password')
        email = data.get('email')
        if not password or not email:
            return jsonify({"message": "Missing email or password"}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM user WHERE password = %s AND email = %s"
        cursor.execute(query, (password, email))
        user = cursor.fetchone()

        cursor.close()

        if user:
            return jsonify({
                "message": "Login successful",
                "user": user
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401

user_view = LoginAPI.as_view('user_api')
login_bp.add_url_rule('/login', view_func=user_view, methods=['POST', 'OPTION'])