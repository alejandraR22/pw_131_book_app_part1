from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(64), primary_key = True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    username = db.Column(db.String(16), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = False)

    books = db.relationship("Book", backref="user")


    def __init__(self, username, password):
        self.id = str(uuid4())
        self.username = username
        self.password = generate_password_hash(password)

    def compare_password(self, password):
        return check_password_hash(self.password, password)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == "password":
                setattr(self, key, generate_password_hash(value))
            else:
                setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "username": self.username,
            "books": [book.to_response() for book in self.books]
        }

class Book(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, author, user_id):
        self.id = str(uuid4())
        self.title = title
        self.author = author
        self.user_id = user_id

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "title": self.title,
            "author": self.author,
            "user_id": self.user_id
        }