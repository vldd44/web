import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.users import User


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
@app.route("/index")
def index():
    session = db_session.create_session()
    result = session.query(User).all()
    return render_template("index.html", result=result)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    login_val = request.form.get("login")
    password = request.form.get("password")

    session = db_session.create_session()
    user = session.query(User).filter(
        (User.email == login_val) | (User.name == login_val)
    ).first()

    if user and user.check_password(password):
        login_user(user)
        return redirect("/")

    return render_template("login.html", error="Неверный логин или пароль")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    app.run("127.0.0.1", 8080)