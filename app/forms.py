import re

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, URLField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Config
from app.validators import image_validation, pdf_validation


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()

        if not user or not user.check_password(self.password.data):
            raise ValidationError('Неверное имя пользователя или пароль.')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Please use a different username.')


class CreateNewsForm(FlaskForm):
    title = StringField("Название поста:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[DataRequired(), image_validation])
    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")


class AddSmiPostForm(FlaskForm):
    title = StringField("Название поста", validators=[DataRequired()])
    url = URLField("Ссылка на пост", validators=[DataRequired()])
    # cover_file = FileField("Файл изображения")
    cover_url = URLField("Ссылка изображения")
    submit = SubmitField("Добавить")

    # def validate_cover_url(self, cover_url):
    #
    #     if (self.cover_file.data and self.cover_url.data) or (not self.cover_file.data and not self.cover_url.data):
    #         raise ValidationError("Выберите ОДИН из вариантов загрузки изображения")


class AddAnimalForm(FlaskForm):
    title = StringField("Кличка нового животного:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[DataRequired(), image_validation])
    body = CKEditorField("Информация о животном:", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class AddPartnerForm(FlaskForm):
    name = StringField("Имя партнёра:", validators=[DataRequired()])
    logo = FileField("Логотип партнёра:", validators=[DataRequired(), image_validation])
    link = URLField("Ссылка на партнёра")
    submit = SubmitField("Добавить")


class AddDocumentForm(FlaskForm):
    title = StringField("Название документа", validators=[DataRequired()])

    document = FileField("Документ", validators=[DataRequired(), pdf_validation])
    submit = SubmitField("Добавить")


class ConfigForm(FlaskForm):
    site_logo = FileField("Логотип сайта", validators=[image_validation])
    background_image = FileField("Фоновое изображение главной страницы", validators=[image_validation])
    allow_background_image = BooleanField("Отображать фоновое изображение")
    save = SubmitField("Сохранить")


class PageDataForm(FlaskForm):
    title = StringField("Заглавие страницы", validators=[DataRequired()])
    description = CKEditorField("Описание страницы", validators=[DataRequired()])
    save = SubmitField("Сохранить")