from flask import Flask, render_template, request, redirect, session, g, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # def set_password(self, password):
    #     self



# users = []
# users.append(User(1, "Jimbo", "password"))
# users.append(User(2, "Jones", "password"))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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


# @app.route("/profile")
# def profile():
#     if not g.user:
#         return redirect(url_for('login'))

#     return render_template("profile.html")

