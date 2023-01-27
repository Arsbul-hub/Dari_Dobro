from flask import render_template, send_from_directory, url_for, render_template_string, flash, redirect
from app import app
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.forms import LoginForm


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template('login.html', title='Sign In', form=form)


@app.route('/reporting')
def reporting():
    return render_template("Отчетность.html")


@app.route('/documents')
def documents():
    return render_template("Уставные документы.html")


@app.route('/smi')
def smi():
    return render_template("СМИ о нас.html")


@app.route('/materials')
def materials():
    return render_template("Полезные материалы.html")


@app.route('/partners')
def partners():
    return render_template("Партнеры.html")


@app.route('/Наши животные')
def our_animals():
    return render_template("Наши животные.html")


@app.route('/Дом для животных')
def house_for_animals():
    return render_template("Дом для животных.html")


@app.route('/Скорая помощь')
def ambulance():
    return render_template("Скорая помощь.html")


@app.route('/Просвещение и мероприятия')
def activities():
    return render_template("Просвещение и мероприятия.html")


@app.route('/Помогите финансово')
def help_money():
    return render_template("Помогите финансово.html")


@app.route('/Стать опекуном')
def opeka():
    return render_template("Стать опекуном.html")


@app.route('/Стать волонтером')
def volunteer():
    return render_template("Стать волонтером.html")


@app.route('/Оставайтесь сытыми')
def full():
    return render_template("Оставайтесь cытыми.html")


@app.route('/Наши сборы')
def fees():
    return render_template("Наши сборы.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.route('/app-ads.txt')
def download_file():
    return render_template_string('''google.com, pub-9371118693960899, DIRECT, f08c47fec0942fa00''')
