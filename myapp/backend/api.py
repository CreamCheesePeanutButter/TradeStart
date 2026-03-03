from flask import Flask, jsonify
from flask_cors import CORS
from sqlconnection import DatabaseConfig

app = Flask(__name__)
CORS(app, origins=["http://localhost:5174"])  # React (Vite)


db_config = DatabaseConfig(
    host="mysql-creamcheesepeanutbutter.alwaysdata.net",
    user="creamcheesepeanutbutter_matt",
    password="ilikepeanutbutter",
    database="creamcheesepeanutbutter_users"
)

@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = db_config.get_users()

        return jsonify(users)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/users", methods=["POST"])
def add_user():
    from flask import request
    try:
        data = request.get_json()
        name = data.get("name")
        age = data.get("age")
        email = data.get("email")

        db_config.add_user(name, age, email)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "User added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
