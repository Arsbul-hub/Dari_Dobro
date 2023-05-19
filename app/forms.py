import re

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, URLField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Config, Documents, Gallery
from app.validators import image_validation, pdf_validation, data_required


class LoginForm(FlaskForm):
    _name = "Вход"
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()

        if not user or not user.check_password(self.password.data):
            raise ValidationError('Неверное имя пользователя или пароль.')


class RegistrationForm(FlaskForm):
    _name = "Регистрация"
    username = StringField('Имя пользователя', validators=[DataRequired()])

    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired()])
    # remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Это имя пользователя занято')

    def validate_password2(self, password):
        if password.data != self.password.data:
            raise ValidationError('Пароли не совпадают')


class CreateNewsForm(FlaskForm):
    _name = "Создать новость"
    title = StringField("Название поста:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[DataRequired(), image_validation])
    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")


class EditNewsForm(FlaskForm):
    _name = "Изменить новость"
    title = StringField("Название поста:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[image_validation])
    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class CreateMaterialsForm(FlaskForm):
    _name = "Добавить материал"
    title = StringField("Название поста:", validators=[DataRequired()])

    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Создать")


class EditMaterialsForm(FlaskForm):
    _name = "Изменить материал"
    title = StringField("Название поста:", validators=[DataRequired()])

    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class AddSmiPostForm(FlaskForm):
    _name = "Добавить пост сми"
    title = StringField("Название поста", validators=[DataRequired()])
    url = URLField("Ссылка на пост", validators=[DataRequired()])
    # cover_file = FileField("Файл изображения")
    cover_url = URLField("Ссылка изображения")
    submit = SubmitField("Добавить")


class EditSmiPostForm(FlaskForm):
    _name = "Изменить пост сми"
    title = StringField("Название поста", validators=[DataRequired()])
    url = URLField("Ссылка на пост", validators=[DataRequired()])
    # cover_file = FileField("Файл изображения")
    cover_url = URLField("Ссылка изображения")
    submit = SubmitField("Сохранить")


class AddAnimalForm(FlaskForm):
    _name = "Добавить животное"
    name = StringField("Кличка нового животного:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[DataRequired(), image_validation])
    body = CKEditorField("Информация о животном:", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class EditAnimalForm(FlaskForm):
    _name = "Изменить животное"
    name = StringField("Кличка нового животного:", validators=[DataRequired()])
    cover = FileField("Фотография:", validators=[image_validation])
    body = CKEditorField("Информация о животном:", validators=[DataRequired()])
    submit = SubmitField("Сохранить")


class AddPartnerForm(FlaskForm):
    _name = "Добавить партнера"
    name = StringField("Имя партнёра:", validators=[DataRequired()])
    logo = FileField("Логотип партнёра:", validators=[DataRequired(), image_validation])
    link = URLField("Ссылка на партнёра")
    submit = SubmitField("Добавить")


class EditPartnerForm(FlaskForm):
    _name = "Изменить партнера"
    name = StringField("Имя партнёра:", validators=[DataRequired()])
    logo = FileField("Логотип партнёра:", validators=[image_validation])
    link = URLField("Ссылка на партнёра")
    submit = SubmitField("Сохранить")


class AddDocumentForm(FlaskForm):
    _name = "Добавить документ"
    title = StringField("Название документа", validators=[DataRequired()])

    document = FileField("Документ", validators=[DataRequired(), pdf_validation])
    submit = SubmitField("Добавить")

    def validate_title(self, title):
        if Documents.query.filter_by(title=title.data).all():
            raise ValidationError("Документ с таким названием уже существует!")


class EditDocumentForm(FlaskForm):
    _name = "Изменить документ"
    title = StringField("Название документа", validators=[DataRequired()])

    document = FileField("Документ", validators=[pdf_validation])
    submit = SubmitField("Сохранить")


class AddImageForm(FlaskForm):
    _name = "Добавить изображение"
    title = StringField("Название изображения", validators=[DataRequired()])

    image = FileField("Изображение", validators=[DataRequired(), image_validation])
    submit = SubmitField("Добавить")

    def validate_title(self, title):
        if Gallery.query.filter_by(title=title.data).all():
            raise ValidationError("Изображение с таким названием уже существует!")


class ConfigForm(FlaskForm):
    _name = "Настройки сайта"
    site_logo = FileField("Логотип сайта", validators=[image_validation])
    background_image = FileField("Фоновое изображение главной страницы", validators=[image_validation])
    allow_background_image = BooleanField("Отображать фоновое изображение")
    save = SubmitField("Сохранить")


class PageDataForm(FlaskForm):
    _name = "Изменить страницу"
    title = StringField("Заглавие страницы", validators=[DataRequired()])
    description = CKEditorField("Описание страницы", validators=[DataRequired()])
    save = SubmitField("Сохранить")
