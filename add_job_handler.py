from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "password1921"

db_session.global_init("db/mars_explorer.db")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    session = db_session.create_session()
    return session.get(User, user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("jobs_list.html", jobs=jobs)


@app.route("/add_job", methods=["GET", "POST"])
@login_required
def add_job():
    if request.method == "GET":
        return render_template("add_job.html")

    session = db_session.create_session()

    job = Jobs()
    job.job = request.form.get("job")
    job.team_leader = int(request.form.get("team_leader"))
    job.work_size = int(request.form.get("work_size"))
    job.collaborators = request.form.get("collaborators")

    start_date = request.form.get("start_date")
    if start_date:
        job.start_date = datetime.strptime(start_date, "%Y-%m-%d")

    end_date = request.form.get("end_date")
    if end_date:
        job.end_date = datetime.strptime(end_date, "%Y-%m-%d")

    job.is_finished = bool(request.form.get("is_finished"))

    session.add(job)
    session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)