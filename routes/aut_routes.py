from flask import Blueprint,request,jsonify
from model import db,User
from schemas import UserSchema
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth",__name__)
user_schema = UserSchema()


@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return ({"error":"Email already registered"}),400
    
    hashed_password = generate_password_hash(data["password"])

    new_user=User(
        username=data["username"],
        email=data["email"],
        password_hash=hashed_password,
        role=data.get("role", "reader")
    )

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user),201

@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data.get("email")).first()


    
    if not user or not check_password_hash(user.password_hash,data["password"]):
        return jsonify({"error":"Invalid credentials"}),401
    

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        "message":"Login Successful",
        "user": user_schema.dump(user),
        "access_token":access_token
    }),200

