import locale
import os

from flask import Flask, Blueprint, session
from flask_ckeditor import CKEditor

from flask_restful import Api

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
import pymorphy3
import flaskfilemanager

application = Flask(__name__)
application.config.from_object(Config)

ckeditor = CKEditor(application)
blueprint = Blueprint('app_api', __name__, template_folder='templates')

db = SQLAlchemy()
db.init_app(application)
migrate = Migrate(application, db, render_as_batch=True)
login = LoginManager(application)
login.login_view = 'login'

morph = pymorphy3.MorphAnalyzer()
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)


def my_access_control_function():
    return current_user.is_authenticated


flaskfilemanager.init(application,
                      custom_config_json_path="static/json/filemanager.config.json",
                      access_control_function=my_access_control_function)

from application import routes, models
