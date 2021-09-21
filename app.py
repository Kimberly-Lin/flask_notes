from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hashing_login"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.get("/")
def redirect_to_register():
    """redirects user to register page"""
    return redirect("/register")


@app.get("/register")
def display_register_form():
    """Show user register form"""
    return render_template("register.html")


@app.post("/register")
def save_register_info_to_server():
    """Take form inputs and saves user to database"""


@app.get("/login")
def show_login_form():
    """Show user login form"""


@app.post("/login")
def process_login():
    """Process login form, saves login user to session"""


@app.get("/secret")
def display_secret_page():
    """Renders secret.html"""
