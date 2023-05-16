from sqlalchemy_serializer import SerializerMixin

from app import db, db_session
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as sa

__basemodel = db.Model


class User(UserMixin, __basemodel):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(), index=True, unique=True)
    password_hash = sa.Column(sa.String(128))

    def __repr__(self):
        return 'Пользователь {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class News(__basemodel, SerializerMixin):
    __tablename__ = 'news'
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String())
    title = sa.Column(sa.String())
    cover = sa.Column(sa.String())
    timestamp = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)
    deleted = sa.Column(sa.Boolean, default=False)


class Materials(__basemodel, SerializerMixin):
    __tablename__ = 'materials'
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String())
    title = sa.Column(sa.String())
    timestamp = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)


class SmiPosts(__basemodel, SerializerMixin):
    __tablename__ = 'smi'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String())
    cover = sa.Column(sa.String())
    url = sa.Column(sa.String())
    timestamp = sa.Column(sa.DateTime, index=True, default=datetime.utcnow)


class Partners(__basemodel):
    __tablename__ = 'partners'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String())
    logo = sa.Column(sa.String())
    link = sa.Column(sa.String())


class Animals(__basemodel):
    __tablename__ = 'animals'
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String())
    name = sa.Column(sa.String())
    cover = sa.Column(sa.String())
    have_house = sa.Column(sa.Boolean, default=False)

    def move_to_house(self):
        self.have_house = True

    def move_to_vet(self):
        self.have_house = False


class Documents(__basemodel):
    __tablename__ = 'documents'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String())
    file = sa.Column(sa.String())


class Gallery(__basemodel):
    __tablename__ = 'gallery'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String())
    file = sa.Column(sa.String())


class Config(__basemodel):
    __tablename__ = 'config'
    name = sa.Column(sa.String(), primary_key=True)
    value = sa.Column(sa.String())


class PagesData(__basemodel):
    __tablename__ = 'pages_data'
    page = sa.Column(sa.String, primary_key=True)
    title = sa.Column(sa.String)
    description = sa.Column(sa.String)
