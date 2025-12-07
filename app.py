from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager   
from dotenv import load_dotenv
import os
app=Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return "Welcome to the Blog API"

if __name__ == '__main__':
    app.run(debug=True) 
