import os
import json
import random
import requests
from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from forms.department_form import DepartmentForm
from forms.Login_form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user
import flask_wtf

from flask_restful import reqparse, abort, Api, Resource

from forms.jobs_form import JobsForm
from forms.registration_form import RegistrationForm
from resources.jobs_resources import JobsResource, JobsListResource
from resources.users_resource import UserResource, UserListResource

app = Flask(__name__)
api = Api(app)
api.add_resource(JobsResource, "/api/v2/jobs/<int:jobs_id>")
api.add_resource(JobsListResource, "/api/v2/jobs")
api.add_resource(UserResource, "/api/v2/users/<int:user_id>")
api.add_resource(UserListResource, "/api/v2/users")

app.config["SECRET_KEY"] = "password1921"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    return render_template("index.html", title="Главная", jobs=jobs, users=users)


@app.route("/distribution")
def distribution():
    astronauts = request.args.getlist("astronauts")
    return render_template("distribution.html", title="Распределение", astronauts=astronauts)


@app.route("/table")
def cabin_table():
    sex = request.args.get("sex", "")
    age = int(request.args.get("age", 0))

    if sex == "male" and age >= 21:
        color = "синий"
    elif sex == "male" and age < 21:
        color = "голубой"
    elif sex == "female" and age >= 21:
        color = "розовый"
    elif sex == "female" and age < 21:
        color = "светло-розовый"
    else:
        color = "белый"

    if age < 21:
        martian_image = "images/mars.png"
    else:
        martian_image = "images/mars_new.png"

    return render_template("table.html", title="Каюта", color=color, martian_image=martian_image)


@app.route("/promotion")
def promotion():
    return """
    <h1>Человечество вырастает из детства.</h1>
    <h2>Человечеству мала одна планета.</h2>
    <h3>Мы сделаем обитаемыми безжизненные пока планеты.</h3>
    <h4>И начнем с Марса!</h4>
    <h1>Присоединяйся!</h1>
    """


@app.route("/image_mars")
def image_mars():
    return render_template("image_mars.html")


@app.route("/promotion_image")
def promotion_image():
    return render_template("promotion_image.html")


@app.route("/mars_gallery", methods=["GET", "POST"])
def mars_gallery():
    default_images = [
        "images/mars.png",
        "images/mars_new.png",
        "images/sci.png",
        "images/ing.png"
    ]

    uploaded_files = []
    upload_dir = os.path.join("static", "images", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    if os.path.exists(upload_dir):
        uploaded_files = [f"images/uploads/{f}" for f in os.listdir(upload_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    images = default_images + uploaded_files

    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            filename = f"img_{len(uploaded_files) + 1}_{file.filename}"
            file.save(os.path.join(upload_dir, filename))

    if request.method == "POST":
        uploaded_files = [f"images/uploads/{f}" for f in os.listdir(upload_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        images = default_images + uploaded_files

    return render_template("mars_gallery.html", title="Галерея Марса", images=images)


@app.route("/member")
def member():
    with open("templates/crew.json", "r", encoding="utf-8") as f:
        crew = json.load(f)
    random_member = random.choice(crew)
    return render_template("member.html", title="Член экипажа", member=random_member)


planet_slovar = {
    "Марс": {
        "description": "Эта планета близка к Земле;",
        "resources": "На ней много необходимых ресурсов;",
        "atmosphere": "На ней есть вода и атмосфера;",
        "magnetic_field": "На ней есть небольшое магнитное поле;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Земля": {
        "description": "Это наша родная планета;",
        "resources": "На ней есть всё, что нужно для жизни;",
        "atmosphere": "На ней есть воздух и вода;",
        "magnetic_field": "На ней есть магнитное поле;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Венера": {
        "description": "Эта планета — жаркий и токсичный мир;",
        "resources": "На ней есть металлы, но в условиях, не подходящих для жизни;",
        "atmosphere": "На ней есть плотная атмосфера из углекислого газа;",
        "magnetic_field": "На ней практически нет магнитного поля;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Юпитер": {
        "description": "Это гигант — самая большая планета;",
        "resources": "На ней есть водород, гелий и другие элементы;",
        "atmosphere": "На ней есть гигантские облака и ветры;",
        "magnetic_field": "На ней есть очень сильное магнитное поле;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Сатурн": {
        "description": "Эта планета известна своими кольцами;",
        "resources": "На ней есть газы и лёд, но не для жизни;",
        "atmosphere": "На ней есть тонкая атмосфера из метана и водорода;",
        "magnetic_field": "На ней есть магнитное поле, но слабее, чем у Юпитера;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Уран": {
        "description": "Эта планета вращается на боку;",
        "resources": "На ней есть водород, гелий и метан;",
        "atmosphere": "На ней есть атмосфера с синим оттенком из метана;",
        "magnetic_field": "На ней есть магнитное поле, но сильно смещено;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Нептун": {
        "description": "Эта планета — холодный и ветренистый мир;",
        "resources": "На ней есть водород, гелий и метан;",
        "atmosphere": "На ней есть сильные ветры и тёмная атмосфера;",
        "magnetic_field": "На ней есть сильное магнитное поле;",
        "beauty": "Наконец, она просто красивая!"
    },
    "Меркурий": {
        "description": "Эта планета — самый близкий к Солнцу;",
        "resources": "На ней есть металлы и редкие элементы;",
        "atmosphere": "На ней почти нет атмосферы;",
        "magnetic_field": "На ней есть слабое магнитное поле;",
        "beauty": "Наконец, она просто красивая!"
    }
}


@app.route("/choice/<planet_name>")
def choice_planet(planet_name):
    return render_template("choice.html", planet_name=planet_name,
                           description=planet_slovar[planet_name]["description"],
                           resources=planet_slovar[planet_name]["resources"],
                           atmosphere=planet_slovar[planet_name]["atmosphere"],
                           magnetic_field=planet_slovar[planet_name]["magnetic_field"],
                           beauty=planet_slovar[planet_name]["beauty"])


@app.route("/results/<nickname>/<int:level>/<float:rating>")
def results(nickname, level, rating):
    return render_template("results.html", nickname=nickname, level=level, rating=rating)


@app.route("/astronaut_selection")
def astronaut_selection():
    return render_template("astronaut_selection.html", title="отбор астронавтов")


@app.route("/training/<prof>")
def training(prof):
    return render_template("training.html", title="", prof=prof)


prof_list = ["пилот", "инженер-исследователь", "инженер-строитель", "врач", "штурман"]


@app.route("/list_prof/<list1>")
def list_prof(list1):
    return render_template("list_prof.html", list=list1, prof_list=prof_list)


@app.route("/answer")
@app.route("/auto_answer")
def answer():
    context = {
        "title": "Анкета",
        "surname": "Watny",
        "name": "Mark",
        "education": "выше среднего",
        "profession": "штурман марсохода",
        "sex": "male",
        "motivation": "Всегда мечтал застрять на Марсе!",
        "ready": True
    }
    return render_template("auto_answer.html", **context)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == request.form.get("email")
        ).first()
        if user and user.check_password(request.form.get("password")):
            remember = bool(request.form.get("remember_me"))
            login_user(user, remember)
            return redirect("/")
        else:
            return render_template("login.html", title="Вход", message="Пользователь не существует.")
    return render_template("login.html", title="Вход")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        db_sess = db_session.create_session()
        new_user = User()
        new_user.surname = registration_form.surname.data
        new_user.name = registration_form.name.data
        new_user.age = registration_form.age.data
        new_user.position = registration_form.position.data
        new_user.speciality = registration_form.speciality.data
        new_user.address = registration_form.address.data
        new_user.email = registration_form.email.data
        new_user.hash_password(registration_form.password.data)
        db_sess.add(new_user)
        db_sess.commit()
        return redirect("/login")

    return render_template("registration.html", form=registration_form, title="Регистрация")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/users_show/<int:user_id>")
def users_show(user_id):
    api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    user_response = requests.get(f"http://127.0.0.1:8080/api/v2/users/{user_id}")
    if user_response.status_code != 200:
        return "User not found", 404

    user = user_response.json()

    if not user.get("city_from"):
        return "City not specified", 400

    geocoder_url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": api_key,
        "geocode": user["city_from"],
        "format": "json"
    }

    geo_response = requests.get(geocoder_url, params=params)
    if geo_response.status_code != 200:
        return "Geocoder error", 500

    geo_data = geo_response.json()
    try:
        pos = geo_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = pos.split()
    except (KeyError, IndexError):
        return "City not found", 404

    return render_template("users_show.html",
                           title=f"{user['surname']} {user['name']} - {user['city_from']}",
                           user=user,
                           city_name=user["city_from"],
                           lat=lat,
                           lon=lon)


@app.route("/addjob", methods=["GET", "POST"])
@app.route("/addjob/<int:job_id>", methods=["GET", "POST"])
@login_required
def add_job(job_id=None):
    db_sess = db_session.create_session()

    if job_id:
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if not job:
            return redirect("/")

        if job.team_leader != current_user.id and current_user.id != 1:
            return redirect("/")

        if request.method == "POST":
            job.job = request.form.get("job")
            job.team_leader = int(request.form.get("team_leader"))
            job.work_size = int(request.form.get("work_size"))
            job.collaborators = request.form.get("collaborators")
            job.is_finished = 1 if request.form.get("is_finished") else 0
            db_sess.commit()
            return redirect("/")

        return render_template("addjob.html", title="Редактирование работы", job=job)

    if request.method == "POST":
        new_job = Jobs()
        new_job.job = request.form.get("job")
        new_job.team_leader = int(request.form.get("team_leader"))
        new_job.work_size = int(request.form.get("work_size"))
        new_job.collaborators = request.form.get("collaborators")
        new_job.is_finished = 1 if request.form.get("is_finished") else 0
        db_sess.add(new_job)
        db_sess.commit()
        return redirect("/")

    return render_template("addjob.html", title="Добавить работу")


@app.route("/jobs/<int:job_id>/delete")
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

    if job:
        if job.team_leader == current_user.id or current_user.id == 1:
            db_sess.delete(job)
            db_sess.commit()

    return redirect("/")


@app.route("/departments")
def departments():
    session = db_session.create_session()
    departments_list = session.query(Department).all()
    return render_template("departments.html", title="Департаменты", departments=departments_list)


@app.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
    if request.method == "POST":
        session = db_session.create_session()
        dept = Department()
        dept.title = request.form.get("title")
        dept.chief = int(request.form.get("chief"))
        dept.members = request.form.get("members")
        dept.email = request.form.get("email")
        session.add(dept)
        session.commit()
        return redirect("/departments")
    return render_template("department_form.html", title="Добавить департамент", department=None)


@app.route("/departments/edit/<int:dept_id>", methods=["GET", "POST"])
@login_required
def edit_department(dept_id):
    session = db_session.create_session()
    dept = session.query(Department).filter(Department.id == dept_id).first()

    if not dept:
        return redirect("/departments")

    if request.method == "POST":
        dept.title = request.form.get("title")
        dept.chief = int(request.form.get("chief"))
        dept.members = request.form.get("members")
        dept.email = request.form.get("email")
        session.commit()
        return redirect("/departments")

    return render_template("department_form.html", title="Редактировать департамент", department=dept)


@app.route("/departments/delete/<int:dept_id>")
@login_required
def delete_department(dept_id):
    session = db_session.create_session()
    dept = session.query(Department).filter(Department.id == dept_id).first()
    if dept:
        session.delete(dept)
        session.commit()
    return redirect("/departments")


@app.route("/load_photo", methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return render_template("load_photo.html")
    else:
        f = request.files['file']
        try:
            f.save("static/images/temp_file.png")
        except Exception as e:
            print(e)
        return render_template("load_photo.html")


@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    pass


@app.route("/jobs/<id>", methods=["GET", "DELETE", "PUT"])
def jobs_red(id):
    pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == "__main__":
    db_session.global_init("db/mars_explorer.db")
    app.run("127.0.0.1", 8080)
