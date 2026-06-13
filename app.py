from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask import jsonify
from exceptions import APIError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from extension import limiter
import os

from flask_jwt_extended import JWTManager   
from dotenv import load_dotenv
import os
app=Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

from model import db

db.init_app(app)


with app.app_context():
    db.create_all()
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
limiter.init_app(app)

from routes.aut_routes import auth_bp
from routes.post_routes import post_bp


app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)

@app.errorhandler(APIError)
def handle_api_error(error):

    return jsonify({
        "error": error.message
    }), error.status_code

@app.route('/')
def home():
    return "Welcome to the Blog API"

if __name__ == '__main__':
    app.run(debug=True) 

def create_app(testing=False):
    app=Flask(__name__)

    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///:memory:"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"

    app.config["JWT_SECRET_KEY"] ="super-secret"
    app.config["TESTING"]=testing

    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)

    return app

print("DATABASE URI =", app.config["SQLALCHEMY_DATABASE_URI"])
import os

print("DB FILE:", os.path.abspath("instance/site.db"))