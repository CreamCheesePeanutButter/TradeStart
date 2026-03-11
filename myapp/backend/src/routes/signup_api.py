from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

signup_bp = Blueprint('signup_api', __name__)

class SignupAPI(MethodView):

    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Missing email or password"}), 400

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # Check if user already exists
        check_query = "SELECT * FROM user WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            return jsonify({"message": "User already exists"}), 409

        # Insert new user
        insert_query = """
        INSERT INTO user (email, password)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (email, password))
        db.commit()

        cursor.close()

        return jsonify({
            "message": "User registered successfully"
        }), 201


signup_view = SignupAPI.as_view('signup_api')
signup_bp.add_url_rule('/register', view_func=signup_view, methods=['POST'])