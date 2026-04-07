from flask import Flask, jsonify
from flask_cors import CORS
from db import close_db
from routes.login_api import login_bp
from routes.stock_api import stock_bp
from routes.signup_api import signup_bp
from const import const
from routes.funds_api import funds_bp
from routes.user_api import user_bp
from routes.admin_api import admin_bp


app = Flask(__name__)

CORS(app) 
app.secret_key = "test"

app.config["MYSQL_HOST"] = const.HOST_NAME
app.config["MYSQL_USER"] = const.USER
app.config["MYSQL_PASSWORD"] = const.PASSWORD
app.config["MYSQL_DB"] = const.DATABASE


app.register_blueprint(login_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(funds_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    
    app.run(debug=True)