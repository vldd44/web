from flask import Flask, render_template, redirect, request
from data import db_session
from data.db_session import create_session
from data.jobs import Jobs
from data.users import User
from forms.JobsForm import JobsForm
from forms.Login_form import LoginForm
import flask_wtf

app = Flask(__name__)

app.config["SECRET_KEY"] = "password1921"


@app.route("/")
@app.route("/index")
def index():
    session = db_session.create_session()
    result = session.query(Jobs, User).join(
        User,
        Jobs.team_leader == User.id
    )
    return render_template("index.html", title="", result=result)


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
        return redirect("/")
    return render_template("login.html", form=login_form)

@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    jobs_form = JobsForm()
    if jobs_form.validate_on_submit():
        job = Jobs(job=jobs_form.job.data,
                   team_leader=jobs_form.team_leader.data,
                   work_size=jobs_form.work_size.data,
                   collaborators=jobs_form.collaborators.data,
                   is_finished=jobs_form.is_finished.data)
        session = create_session()
        session.add(job)
        session.commit()
        session.close()
        return redirect('/')
    else:
        return render_template('addjob.html',
                               title='Adding a job', form=jobs_form)

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


if __name__ == "__main__":
    db_session.global_init("db/mars_explorer.db")
    app.run("127.0.0.1", 8080)
