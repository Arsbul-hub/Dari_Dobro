from app import db, login
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return 'Пользователь {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    title = db.Column(db.String())
    cover = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)


class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    logo = db.Column(db.String())


class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    name = db.Column(db.String())
    cover = db.Column(db.String())
    have_house = db.Column(db.Boolean, default=False)

    def move_to_house(self):
        self.have_house = True

    def move_to_vet(self):
        self.have_house = False


class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    ref = db.Column(db.String())


class Config(db.Model):
    name = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String())
