from flask import request, Blueprint, jsonify
from flask.views import MethodView
from db import get_db

signup_bp = Blueprint('signup_api', __name__)

class SignupAPI(MethodView):

    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        username = data.get('username', '')

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
        CALL AddNewUser(%s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (email, password, first_name, last_name, username))
        db.commit()

        user_id = cursor.lastrowid
        cursor.close()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user_id
        }), 201


signup_view = SignupAPI.as_view('signup_api')
signup_bp.add_url_rule('/signup', view_func=signup_view, methods=['POST'])