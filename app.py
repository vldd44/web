from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.Login_form import LoginForm
from flask_login import LoginManager, login_user, login_required, logout_user
import flask_wtf

from flask_restful import reqparse, abort, Api, Resource

# from api import api

from forms.jobs_form import JobsForm
from forms.registration_form import RegistrationForm
from resources.jobs_resources import JobsResource, JobsListResource
from resources.users_resource import UserResource, UserListResource

app = Flask(__name__)
# app.register_blueprint(api)
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
    result = session.query(Jobs, User).join(
        User,
        Jobs.team_leader == User.id
    )
    for i in result:
        print(i)
    return render_template("index.html", title="Это база", result=result)


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
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == login_form.email.data
        ).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect("/")
        else:
            return render_template("login.html", form=login_form,
                                   message="Пользователь не существует.")
    return render_template("login.html", form=login_form)


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


@app.route("/addjob", methods=["GET", "POST"])
@login_required
def add_job():
    jobs_form = JobsForm()
    if jobs_form.validate_on_submit():
        db_sess = db_session.create_session()
        new_job = Jobs()
        new_job.job = jobs_form.job.data
        new_job.team_leader = jobs_form.team_leader.data
        new_job.work_size = jobs_form.work_size.data
        new_job.collaborators = jobs_form.collaborators.data
        if jobs_form.is_finished.data:
            new_job.is_finished = 1
        else:
            new_job.is_finished = 0
        db_sess.add(new_job)
        db_sess.commit()
        return redirect("/")
    return render_template("addjob.html", form=jobs_form, title="Adding a job")


@app.route("/load_photo", methods=['POST', 'GET'])
def load_photo():
    if request.method == 'GET':
        return render_template("load_photo.html")
    else:
        f = request.files['file']
        try:
            with open("/static/images/temp_file.png", mode="wb") as fili:
                fili.save(f)
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
