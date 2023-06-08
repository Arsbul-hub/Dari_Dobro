import os
import string

from flask import render_template, send_from_directory, url_for, flash, redirect, request
from flask_ckeditor import upload_fail, upload_success
from app import application, morph
from PIL import Image
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from app.forms import *
from werkzeug.urls import url_parse
from app import login
from flask import session
import random
from bs4 import BeautifulSoup


def load_file(name):
    try:
        return Image.open("app/" + name)

    except FileNotFoundError:
        return None


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@application.route('/files/<path:filename>')
def uploaded_files(filename):
    return send_from_directory("static/loaded_media", filename)


@application.route('/reload_auth')
def reload_auth_system():
    messages = ["Конфигурационный файл аутентификации пользователей был перезагружен!"]
    admin = User.query.filter_by(username="Admin").first()
    if admin:
        admin.username = application.config["DEFAULT_ADMIN_USERNAME"]
        admin.set_password(application.config["DEFAULT_ADMIN_PASSWORD"])

    else:
        admin = User()
        admin.username = application.config["DEFAULT_ADMIN_USERNAME"]
        admin.set_password(application.config["DEFAULT_ADMIN_PASSWORD"])
        db.session.add(admin)

    db.session.commit()
    logout_user()

    return render_template("service/Уведомление.html", title="Внимание", messages=messages)


@application.route('/upload', methods=['POST', "GET"])
def upload():
    f = request.files.get('upload')
    # Add more validations here
    save_file(f)

    url = url_for('uploaded_files', filename=f.filename)

    return upload_success(url, filename=f.filename)


def namegen(size=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def save_file(file, path="", name=None, formates=[], service_path=""):
    full_path = "static/loaded_media"
    extension = file.filename.split('.')[-1].lower()
    file.filename = namegen(8).replace(" ", "") + "." + extension
    if service_path:
        full_path = f"static/{service_path}"

    if not file:
        return None
    if name:
        file.filename = name.replace(' ', '')
    if path and not os.path.exists(f"app/static/loaded_media/{path}"):
        os.makedirs(f"app/static/loaded_media/{path}")

    if "image" in file.content_type:
        image = Image.open(file)
        if image.width > 2000:
            require_width = 2000  # Уменьшенный размер (ширина)
            new_size = require_width, int((float(image.size[1]) * float((require_width / float(image.size[0])))))
            image = image.resize(new_size, Image.LANCZOS)

        elif image.height > 1300:
            require_height = 1300  # Уменьшенный размер (высота)
            new_size = int((float(image.size[0]) * float((require_height / float(image.size[1]))))), require_height
            image = image.resize(new_size, Image.LANCZOS)
        image.save(f"app/{full_path}/{path}/{file.filename}")
    else:
        file.save(f"app/{full_path}/{path}/{file.filename}")
    return f"static/loaded_media/{path}/{file.filename}"


def remove_file(path):
    if os.path.exists("app/" + path):
        os.remove("app/" + path)


@application.route('/')
def index():
    data = PagesData.query.get("index")
    allow_background_image = False
    site_name = ""
    if Config.query.filter_by(category="config").all():
        allow_background_image = Config.query.get("allow_background_image").value
        site_name = Config.query.get("site_name").value
    return render_template("index.html", user=current_user, site_data=data, site_name=site_name,
                           allow_background_image=allow_background_image)


@application.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@application.route("/delete_user")
@login_required
def delete_user():
    user = User.query.get(request.args.get("id"))
    if user and user.username != application.config["DEFAULT_ADMIN_USERNAME"]:
        logout_user()
        db.session.delete(user)
        db.session.commit()
    return redirect("/")


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if session.get("wrong_password_date") and (
            datetime.now() - datetime.fromisoformat(session["wrong_password_date"])).seconds >= 5 * 60:
        session.pop("wrong_password_date")
        session.pop("wrong_passwords")
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else:
        session["wrong_passwords"] = 0
    return render_template('forms/login.html', user=current_user, title='Sign In', form=form)


@application.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # login_user(user, remember=form.remember_me.data)
        flash('Congratulations, you are now a registered admin!')
        return redirect(url_for('index'))
    return render_template('forms/register.html', user=current_user, title='Register', form=form)


@application.route("/admin_panel")
@login_required
def admin_panel():
    # Я хотел делать бэкапы, но не вышло
    # action = request.args.get("action")
    # if action == "get_backup":
    #     n = datetime.now()
    #     with ZipFile(f"application/static/backups/backup-{n.year}-{n.month}-{n.day}-{n.hour}-{n.minute}-{n.second}.zip", "w") as zip_file:
    #         zip_file.write("./application.db")
    #         for resource in pathlib.Path("application/static/loaded_media/").iterdir():
    #             zip_file.write(resource, arcname=f"media/{resource.key}")
    #     send_from_directory("static/backups", f"backup-{n.year}-{n.month}-{n.day}-{n.hour}-{n.minute}-{n.second}.zip", as_attachment=True)

    return render_template("admin_panel.html", user=current_user,
                           admin_username=application.config["DEFAULT_ADMIN_USERNAME"])


@application.route("/site_settings", methods=["GET", "POST"])
@login_required
def site_settings():
    form = ConfigForm()

    if form.validate_on_submit():

        save_file(file=form.site_logo.data, service_path="images", name="logo.png",
                  formates=["png", "jpg", "jpeg", "webp"])
        save_file(file=form.background_image.data, service_path="images", name="background_image.png",
                  formates=["png", "jpg", "jpeg", "webp"])

        Config.query.get("allow_background_image").value = form.allow_background_image.data
        Config.query.get("site_name").value = form.site_name.data
        db.session.commit()
        return redirect(url_for("admin_panel"))
    else:
        if Config.query.filter_by(category="config").all():
            form.allow_background_image.data = int(Config.query.get("allow_background_image").value)
            form.site_name.data = Config.query.get("site_name").value
        else:
            db.session.add(Config(key="allow_background_image", value=False, category="config"))
            db.session.add(Config(key="site_name", value="", category="config"))
            db.session.commit()
    return render_template("forms/site_settings.html", user=current_user, config=Config, form=form)


# @login_required
# @application.route("/Файловый менеджер")
# def file_manager():
#     filemanager_link = url_for('flaskfilemanager.index')
#     print(filemanager_link)
#     return redirect(filemanager_link)


@application.route("/edit_page", methods=["GET", "POST"])
@login_required
def edit_page_description():
    form = PageDataForm()
    page = request.args.get("page")
    page_name = request.args.get("page_name")
    if form.validate_on_submit():
        if PagesData.query.get(page):
            data = PagesData.query.get(page)
            data.description = form.description.data
            data.title = form.title.data
        else:
            data = PagesData()
            data.page = page
            data.description = form.description.data
            data.title = form.title.data
            db.session.add(data)
        db.session.commit()
        return redirect(url_for(page))
    elif PagesData.query.get(page):
        form.description.data = PagesData.query.get(page).description

        form.title.data = PagesData.query.get(page).title
    return render_template("forms/edit_page_description.html", user=current_user, form=form, page_name=page_name)


@application.route("/add_news", methods=['GET', 'POST'])
@login_required
def add_news():
    action = request.args.get("action")

    form = CreateNewsForm()
    if action == "edit":
        form = EditNewsForm()
        news_post = News.query.get(request.args.get("id"))
        if news_post:
            if form.validate_on_submit():
                news_post.title = form.title.data
                news_post.body = form.body.data
                if form.cover.data:
                    news_post.cover = save_file(form.cover.data)
                db.session.commit()
                return redirect(url_for("news"))
            else:
                form.title.data = news_post.title
                form.body.data = news_post.body
        else:
            return redirect(url_for("news"))
    elif form.validate_on_submit():
        saved_cover = save_file(file=form.cover.data, formates=["png", "jpg", "jpeg", "webp"])
        news_post = News(title=form.title.data, body=form.body.data, cover=saved_cover)
        db.session.add(news_post)
        db.session.commit()
        flash('Вы опубликовали новый пост!')
        return redirect(url_for("news"))
    return render_template("forms/add_news.html", user=current_user, form=form)


@application.route("/news")
def news():
    action = request.args.get('action')

    if action == "show":
        news_list = News.query.get(request.args.get('id'))
        return render_template("show_news.html", user=current_user, news=news_list)
    elif current_user.is_authenticated and action == "remove":
        news = News.query.get(request.args.get('id'))
        remove_file(news.cover)
        db.session.delete(news)

        db.session.commit()
        return redirect(url_for("news"))

    news = News.query.all()

    news_list = list(filter(lambda n: (datetime.today() - n.timestamp).total_seconds() < 3600 * 24 * 10, news))
    old_news_list = list(filter(lambda n: (datetime.today() - n.timestamp).total_seconds() > 3600 * 24 * 10, news))

    return render_template("news.html", user=current_user, BeautifulSoup=BeautifulSoup, news=news_list,
                           old_news=old_news_list,
                           morph=morph, today=datetime.today(),
                           case={"gent"})


@application.route("/add_document", methods=['GET', 'POST'])
@login_required
def add_document():
    action = request.args.get("action")
    form = AddDocumentForm()
    if action == "edit":
        form = EditDocumentForm()
        document = Documents.query.get(request.args.get("id"))
        if document:
            if form.validate_on_submit():
                document.title = form.title.data
                if form.document.data:
                    document.file = save_file(form.document.data)

                db.session.commit()
                return redirect(url_for("documents"))
            else:
                form.title.data = document.title
        else:
            return redirect(url_for("documents"))
    elif form.validate_on_submit():
        file = save_file(file=form.document.data, formates=["pdf", "pptx"])
        new_document = Documents(title=form.title.data, file=file)
        db.session.add(new_document)
        db.session.commit()
        flash('Вы добавили новый документ!')
        return redirect(url_for("documents"))
    return render_template("forms/add_document.html", user=current_user, form=form)


@application.route('/documents')
def documents():
    documents_list = Documents.query.all()
    action = request.args.get('action')
    if action == "show":
        document = Documents.get(request.args.get('id'))
        return redirect(document.file)
    elif current_user.is_authenticated:
        if action == "remove":
            db.session.delete(Documents.query.get(request.args.get('id')))
            db.session.commit()
            return redirect(url_for("documents"))
    return render_template("documents.html", user=current_user, documents=documents_list)


@application.route('/smi')
def smi():
    action = request.args.get("action")

    if current_user.is_authenticated and action == "remove":
        db.session.delete(SmiPosts.query.get(request.args.get('id')))

        db.session.commit()
        return redirect(url_for("smi"))

    posts = SmiPosts.query.all()

    return render_template("smi_posts.html", user=current_user, posts=posts, today=datetime.today())


@application.route("/add_smi_post", methods=['GET', 'POST'])
@login_required
def add_smi_post():
    action = request.args.get("action")
    form = AddSmiPostForm()

    if action == "edit":
        form = EditSmiPostForm()
        post = SmiPosts.query.get(request.args.get("id"))
        if post:
            if form.validate_on_submit():
                post.title = form.title.data
                post.cover = form.cover_url.data
                post.url = form.url.data
                db.session.commit()
                return redirect(url_for("smi"))
            else:
                form.title.data = post.title
                form.cover_url.data = post.cover
                form.url.data = post.url
        else:
            return redirect(url_for("smi"))
    elif form.validate_on_submit():
        saved_cover = form.cover_url.data

        smi_post = SmiPosts(title=form.title.data, cover=saved_cover, url=form.url.data)
        db.session.add(smi_post)
        db.session.commit()
        flash('Вы опубликовали новый пост!')
        return redirect(url_for("smi"))
    return render_template("forms/add_smi_post.html", user=current_user, form=form)


@application.route("/add_information", methods=['GET', 'POST'])
@login_required
def add_materials():
    action = request.args.get("action")

    form = CreateMaterialsForm()
    if action == "edit":
        form = EditMaterialsForm()
        material = Materials.query.get(request.args.get("id"))
        if material:
            if form.validate_on_submit():
                material.title = form.title.data
                material.body = form.body.data
                db.session.commit()
                return redirect(url_for("materials"))
            else:
                form.title.data = material.title
                form.body.data = material.body
        else:
            return redirect(url_for("materials"))
    elif form.validate_on_submit():
        new_materials = Materials()
        new_materials.title = form.title.data
        new_materials.body = form.body.data
        db.session.add(new_materials)
        db.session.commit()

        return redirect(url_for("materials"))
    return render_template("forms/add_materials.html", user=current_user, form=form)


@application.route("/information")
def materials():
    action = request.args.get('action')

    print(action)

    if current_user.is_authenticated and action == "remove":
        db.session.query(Materials).filter_by(id=request.args.get('id')).delete()

        db.session.commit()
        return redirect(url_for("materials"))

    return render_template("materials.html", user=current_user, materials_list=Materials.query.all())


@application.route('/partners')
def partners():
    action = request.args.get('action')
    partners = Partners.query.all()
    # partners_desktop = []
    # for i in range(0, len(partners), 2):
    #     partners_desktop.append(partners[i:i + 2])

    if current_user.is_authenticated and action:
        if action == "remove":
            db.session.delete(Partners.query.get(request.args.get('id')))

            db.session.commit()
        return redirect(url_for("partners"))
    return render_template("partners.html", len=len, partners=partners, partners_mobile=partners,
                           user=current_user)


@application.route("/add_partner", methods=['GET', 'POST'])
@login_required
def add_partner():
    action = request.args.get("action")
    form = AddPartnerForm()
    if action == "edit":
        form = EditPartnerForm()
        partner = Partners.query.get(request.args.get("id"))
        if partner:
            if form.validate_on_submit():
                partner.name = form.name.data
                partner.link = form.link.data
                if form.logo.data:
                    partner.logo = save_file(form.logo.data)

                db.session.commit()
                return redirect(url_for("partners"))
            else:
                form.name.data = partner.name
                form.link.data = partner.link
        else:
            return redirect(url_for("partners"))
    elif form.validate_on_submit():
        out_path = save_file(file=form.logo.data)

        new_animal = Partners(name=form.name.data, logo=out_path, link=form.link.data)
        db.session.add(new_animal)
        db.session.commit()
        flash('Вы добавили нового партнёра!')
        return redirect(url_for("partners"))
    return render_template("forms/add_partner.html", user=current_user, form=form)


@application.route("/add_animal", methods=['GET', 'POST'])
@login_required
def add_animal():
    action = request.args.get("action")

    form = AddAnimalForm()
    if action == "edit":
        form = EditAnimalForm()
        animal = Animals.query.get(request.args.get("id"))
        if animal:
            if form.validate_on_submit():
                animal.name = form.name.data
                animal.body = form.body.data
                animal.animal_type = form.animal_type.data
                animal.age_type = form.age.data
                animal.gender = form.gender.data
                if form.cover.data:
                    animal.cover = save_file(form.cover.data)
                db.session.commit()
                return redirect(request.args.get("previous"))
            else:
                form.name.data = animal.name
                form.body.data = animal.body

                form.animal_type.data = animal.animal_type
                form.age.data = animal.age_type
                form.gender.data = animal.gender
        else:
            return redirect(url_for("our_animals", gender=form.gender.data, animal_type=form.animal_type.data))
    elif form.validate_on_submit():
        out_path = save_file(file=form.cover.data)

        new_animal = Animals(name=form.name.data, gender=form.gender.data, animal_type=form.animal_type.data,
                             age_type=form.age.data, body=form.body.data, cover=out_path)
        db.session.add(new_animal)
        db.session.commit()
        flash('Вы добавили новое животное!')
        return redirect(
            url_for("our_animals", gender=form.gender.data, animal_type=form.animal_type.data))
    return render_template("forms/add_animal.html", user=current_user, form=form)


@application.route('/our_animals')
def our_animals():
    action = request.args.get('action')
    gender = request.args.get("gender")
    animal_type = request.args.get("animal_type")

    if current_user.is_authenticated and action:
        if action == "remove":
            db.session.delete(Animals.query.get(request.args.get('id')))

            db.session.commit()
        if action == "move_to_house":
            animal = Animals.query.get(request.args.get('id'))
            animal.move_to_house()
            db.session.commit()

        if action == "move_to_vet":
            animal = Animals.query.get(request.args.get('id'))
            animal.move_to_vet()

            db.session.commit()
        return redirect(request.args.get("previous"))

    if gender and not animal_type:
        return render_template("choose_animal_type.html", gender=gender, user=current_user)

    animals = Animals.query.filter_by(have_house=False, animal_type=animal_type, gender=gender).all()
    no_animals = Animals.query.filter_by(have_house=True, animal_type=animal_type, gender=gender).all()

    return render_template("our_animals.html", BeautifulSoup=BeautifulSoup, animals=animals, no_animals=no_animals,
                           user=current_user)


@application.route("/add_image", methods=['GET', 'POST'])
@login_required
def add_image_to_gallery():
    action = request.args.get("action")
    form = AddImageForm()

    if form.validate_on_submit():
        out_path = save_file(file=form.image.data)
        image = Gallery(title=form.title.data, file=out_path)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for("gallery"))
    return render_template("forms/add_image.html", user=current_user, form=form)


@application.route("/gallery")
def gallery():
    action = request.args.get('action')
    if current_user.is_authenticated and action:
        if action == "remove":
            image = Gallery.query.get(request.args.get('id'))
            db.session.delete(image)
            remove_file(image.file)
            db.session.commit()

        return redirect(url_for("gallery"))

    return render_template("gallery.html", user=current_user, gallery_list=Gallery.query.all())


@application.route("/edit_contacts", methods=["GET", "POST"])
@login_required
def edit_contacts():
    form = EditContacts()
    if form.validate_on_submit():
        if Config.query.filter_by(category="contacts").all():
            Config.query.get("email").value = form.email.data
            Config.query.get("phone_number").value = form.phone.data
            Config.query.get("vk_url").value = form.vk.data
            Config.query.get("ok_url").value = form.ok.data
            Config.query.get("dzen_url").value = form.dzen.data
        else:
            db.session.add(Config(key="email", value=form.email.data, category="contacts"))

            db.session.add(Config(key="phone_number", value=form.phone.data, category="contacts"))
            db.session.add(Config(key="vk_url", value=form.vk.data, category="contacts"))
            db.session.add(Config(key="ok_url", value=form.ok.data, category="contacts"))
            db.session.add(Config(key="dzen_url", value=form.dzen.data, category="contacts"))
        db.session.commit()
        return redirect(url_for("contacts"))
    else:

        if Config.query.filter_by(category="contacts").all():
            form.email.data = Config.query.get("email").value
            form.phone.data = Config.query.get("phone_number").value
            form.vk.data = Config.query.get("vk_url").value
            form.ok.data = Config.query.get("ok_url").value
            form.dzen.data = Config.query.get("dzen_url").value
    return render_template("forms/edit_contacts.html", user=current_user, form=form)


@application.route("/contacts")
def contacts():
    email, phone_number, vk, ok, dzen = "", "", "", "", ""
    if Config.query.filter_by(category="contacts").all():
        email = Config.query.get("email").value
        phone_number = Config.query.get("phone_number").value
        vk = Config.query.get("vk_url").value
        ok = Config.query.get("ok_url").value
        dzen = Config.query.get("dzen_url").value
    return render_template("contacts.html", user=current_user, email=email, phone_number=phone_number, vk=vk, ok=ok,
                           dzen=dzen)


# @login_required
# @application.route("/Добавить социальную сеть", methods=["GET", "POST"])
# def add_social_network():
#     form = AddSocialNetwork()
#     if form.validate_on_submit():
#         social_network = SocialNetworks(name=form.name.data, description=form.description.data, url=form.url.data)
#         db.session.add(social_network)
#         db.session.commit()
#         return redirect(url_for("contacts"))
#     return render_template("forms/add_social_network.html", user=current_user, form=form)
#

# @application.route('/Мероприятия')
# def activities():
#     return redirect("/")

@application.route('/help_money')
def help_money():
    data = PagesData.query.get("help_money")

    return render_template("help_money.html", user=current_user, site_data=data)


@application.route('/opeka')
def opeka():
    data = PagesData.query.get("opeka")

    return render_template("opeka.html", user=current_user, site_data=data)


@application.route('/volunteer')
def volunteer():
    data = PagesData.query.get("volunteer")
    return render_template("volunteer.html", user=current_user, site_data=data)


@application.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', user=current_user), 404


@application.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html', user=current_user), 500
