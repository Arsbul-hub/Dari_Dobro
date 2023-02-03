from flask import Flask
from flask_ckeditor import CKEditor

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'
from app import routes, models
