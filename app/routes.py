from datetime import datetime
import os

from flask import render_template, send_from_directory, url_for, render_template_string, flash, redirect, request
from flask_ckeditor import upload_fail, upload_success

from app import app, db, morph
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, News, Animals, Documents, Config, Partners
from app.forms import LoginForm, RegistrationForm, CreateNewsForm, AddAnimalForm, AddDocumentForm, ConfigForm, \
    AddPartnerForm
from werkzeug.urls import url_parse
from app import login

from urllib.parse import unquote

from bs4 import BeautifulSoup


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/files/<path:filename>')
def uploaded_files(filename):
    return send_from_directory("static/loaded_media", filename)


@app.route('/upload', methods=['POST', "GET"])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    save_file(f)

    url = url_for('uploaded_files', filename=f.filename)

    return upload_success(url, filename=f.filename)


def save_file(file, path="/loaded_media", name=None, formates=[]):
    if not file:
        return None
    if name:
        file.filename = name
    extension = file.filename.split('.')[-1].lower()
    if formates and extension not in formates:
        return upload_fail(message='Image only!')

    file.save(f"app/static/{path}/{file.filename}")
    return f"static/{path}/{file.filename}"


@app.route('/')
def index():
    site_description = Config.query.filter_by(name="description").first()

    if site_description:
        description = site_description.value

    else:
        description = "Описание не задано"

    return render_template("index.html", description=description,
                           allow_background_image=Config.query.filter_by(name="allow_background_image").first().value)


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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, admin=True)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # login_user(user, remember=form.remember_me.data)
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route("/Профиль")
@login_required
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    return render_template("Профиль.html", user=current_user)


@app.route("/Настройки сайта", methods=["GET", "POST"])
@login_required
def site_settings():
    form = ConfigForm()

    if form.validate_on_submit():
        save_file(file=form.site_logo.data, path="images", name="logo.png", formates=["png", "jpg", "jpeg", "webp"])
        save_file(file=form.background_image.data, path="images", name="background_image.png",
                  formates=["png", "jpg", "jpeg", "webp"])

        Config.query.filter_by(name=form.description.name).first().value = form.description.data
        Config.query.filter_by(name=form.allow_background_image.name).first().value = form.allow_background_image.data
        db.session.commit()
        return redirect(url_for("profile"))
    else:
        form.description.data = Config.query.filter_by(name="description").first().value

        form.allow_background_image.data = int(Config.query.filter_by(name="allow_background_image").first().value)
    return render_template("Настройки сайта.html", config=Config, form=form)


@app.route("/Добавить новость", methods=['GET', 'POST'])
@login_required
def add_news():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = CreateNewsForm()
    if form.validate_on_submit():
        saved_cover = save_file(file=form.cover.data, formates=["png", "jpg", "jpeg", "webp"])
        news_post = News(title=form.title.data, body=form.body.data, cover=saved_cover)
        db.session.add(news_post)
        db.session.commit()
        flash('Вы опубликовали новый пост!')
        return redirect(url_for("news"))
    return render_template("Добавить новость.html", form=form)


@app.route("/Новости")
def news():
    action = request.args.get('action')
    if action == "show":
        news_list = News.query.filter_by(id=request.args.get('id')).first()
        return render_template("Новость.html", news=news_list)
    elif current_user.is_authenticated and action:
        if action == "remove":
            News.query.filter_by(id=request.args.get('id')).delete()

            db.session.commit()
        return redirect(url_for("news"))
    news = News.query.all()

    news_list = list(filter(lambda n: (datetime.today() - n.timestamp).total_seconds() < 3600 * 24 * 10, news))
    old_news_list = list(filter(lambda n: (datetime.today() - n.timestamp).total_seconds() > 3600 * 24 * 10, news))
    for i in news_list:
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    return render_template("Новости.html", beautiful_soup=BeautifulSoup, news=news_list, old_news=old_news_list,
                           morph=morph, today=datetime.today(),
                           case={"gent"},
                           user=current_user)


@app.route('/Отчётность')
def reporting():
    return render_template("Отчетность.html")


@app.route("/Добавить документ", methods=['GET', 'POST'])
@login_required
def add_document():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = AddDocumentForm()
    if form.validate_on_submit():
        print(form.document.data)
        file = save_file(file=form.document.data, formates=["pdf", "pptx"])
        new_document = Documents(title=form.title.data, ref=file)
        db.session.add(new_document)
        db.session.commit()
        flash('Вы добавили новый документ!')
        return redirect(url_for("documents"))
    return render_template("Добавить документ.html", form=form)


@app.route('/Документы')
def documents():
    documents_list = Documents.query.all()
    action = request.args.get('action')
    if action == "show":
        document = Documents.query.filter_by(id=request.args.get('id')).first()
        return redirect(document.ref)
    elif current_user.is_authenticated:
        if action == "remove":
            Documents.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            return redirect(url_for("documents"))
    return render_template("Уставные документы.html", documents=documents_list, user=current_user)


@app.route('/Сми')
@login_required
def smi():
    return render_template("СМИ о нас.html")


@app.route('/Материалы')
def materials():
    return render_template("Полезные материалы.html")


@app.route('/Партнёры')
def partners():
    action = request.args.get('action')
    partners = Partners.query.all()
    partners_desktop = []
    for i in range(0, len(partners), 2):
        partners_desktop.append(partners[i:i + 2])

    if current_user.is_authenticated and action:
        if action == "remove":
            Partners.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
        return redirect(url_for("partners"))
    return render_template("Партнеры.html", len=len, partners_desktop=partners_desktop, partners_mobile=partners,
                           user=current_user)


@app.route("/Добавить партнёра", methods=['GET', 'POST'])
@login_required
def add_partner():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = AddPartnerForm()

    if form.validate_on_submit():
        out_path = save_file(file=form.logo.data, formates=["png", "jpg", "jpeg", "webp"])

        new_animal = Partners(name=form.name.data, logo=out_path, link=form.link.data)
        db.session.add(new_animal)
        db.session.commit()
        flash('Вы добавили нового партнёра!')
        return redirect(url_for("partners"))
    return render_template("Добавить партнёра.html", form=form)


@app.route("/Добавить животное", methods=['GET', 'POST'])
@login_required
def add_animal():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = AddAnimalForm()
    if form.validate_on_submit():
        out_path = save_file(file=form.cover.data, formates=["png", "jpg", "jpeg", "webp"])

        new_animal = Animals(name=form.title.data, body=form.body.data, cover=out_path)
        db.session.add(new_animal)
        db.session.commit()
        flash('Вы добавили новое животное!')
        return redirect(url_for("our_animals"))
    return render_template("Добавить животное.html", form=form)


@app.route('/Наши животные')
def our_animals():
    action = request.args.get('action')
    if action == "show":
        animal = Animals.query.filter_by(id=request.args.get('id')).first()
        return render_template("Животное.html", animal=animal)
    elif current_user.is_authenticated and action:
        if action == "remove":
            Animals.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
        if action == "move_to_house":
            animal = Animals.query.filter_by(id=request.args.get('id')).first()
            animal.move_to_house()
            db.session.commit()

        if action == "move_to_vet":
            animal = Animals.query.filter_by(id=request.args.get('id')).first()
            animal.move_to_vet()

            db.session.commit()
        return redirect(url_for("our_animals"))
    animals = Animals.query.filter_by(have_house=False).all()
    no_animals = Animals.query.filter_by(have_house=True).all()
    animals.reverse()
    return render_template("Наши животные.html", animals=animals, no_animals=no_animals, user=current_user)


@app.route("/Контакты")
def contacts():
    # mail = Config.query.filter_by(name="contact_mail").first()
    # grope_vk = Config.query.filter_by(name="contact_vk_link").first()
    return render_template("Контакты.html")


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
