from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Model is a base class in SQLAlchemy that helps to create database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    role = db.Column(db.String(20), default="reader")

    def __repr__ (self):
        return f"User{self.username}"
    

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    content = db.Column(db.Text,nullable=False)

    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    

    def __repr__(self):
        return f"<Post {self.title}>"    





