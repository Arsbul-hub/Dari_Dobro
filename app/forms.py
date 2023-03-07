from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


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
    cover = StringField("Обложка для новости (ссылка):", validators=[DataRequired()])
    body = CKEditorField("Текст поста:", validators=[DataRequired()])
    submit = SubmitField("Опубликовать")


class AddAnimalForm(FlaskForm):
    title = StringField("Кличка нового животного:", validators=[DataRequired()])
    cover = StringField("Фотография (ссылка):", validators=[DataRequired()])
    body = CKEditorField("Информация о животном:", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class AddDocumentForm(FlaskForm):
    title = StringField("Название документа", validators=[DataRequired()])

    ref = StringField("Ссылка на документ (Яндекс диск или Google Диск)", validators=[DataRequired()])
    submit = SubmitField("Добавить")
