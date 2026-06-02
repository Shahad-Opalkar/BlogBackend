from flask_marshmallow import Marshmallow
from model import User, Post

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True

    author = ma.Nested(UserSchema, only=("id", "username"))
