import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'app.db')

    FLASKFILEMANAGER_FILE_PATH = "app/static/loaded_media"

    # FLASKFILEMANAGER_CUSTOM_CONFIG_JSON_PATH = "app/static/json/filemanager.config.json"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_HEIGHT = 500
    CKEDITOR_FILE_UPLOADER = "upload"
    with open("app/static/json/admin_user.json", "r") as f:
        j = json.load(f)
        DEFAULT_ADMIN_USERNAME = j["username"]
        DEFAULT_ADMIN_PASSWORD = j["password"]
