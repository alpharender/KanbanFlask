from flask import Flask, render_template, request, redirect, session, g, url_for
# from flask.ext.login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secretkey"


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User: {self.username}"



users = []
users.append(User(1, "Jimbo", "password"))
users.append(User(2, "Jones", "password"))

@app.route("/")
def index():
    return render_template("index.html")


@app.before_request
def before_request():
    if "user_id" in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop('user_id', None)
        username = request.form["username"]
        password = request.form["password"]

        user = [x for x in users if x.username == username][0] #assumes unique usernames

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for("profile"))

        return redirect(url_for('login'))

    return render_template("login.html")


@app.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template("profile.html")

