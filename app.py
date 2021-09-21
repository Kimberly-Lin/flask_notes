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



@app.route("/register", methods=["GET", "POST"])
def display_and_handle_register_form():
    """If no form inputs or inputs invalid: show user register form
        If inputs are valid, create and add new user to db, and redirect to /secret
    """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        # QUESTION - password = form.password.data  if stored to a variable, is it accessable?
        first_name = form.first_name.data
        last_name = form.last_name.data


        new_user = User.register(username, form.password.data, first_name, last_name, email)
        # new_user["email"]=email 
        # new_user["first_name"]=first_name
        # new_user["last_name"]=last_name

        db.session.add(new_user)
        db.session.commit()

        session["username"] = username 

        return redirect("/secret")
    
    return render_template("register.html", form=form)
    

@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    """Show user login form"""
    """Process login form, saves login user to session"""

    form=LoginForm()

    if form.validate_on_submit():
        username=form.username.data

        curr_user = User.authenticate(username, form.password.data)
        
        if not(curr_user):
            return render_template("login.html", form=form)

        session["username"] = curr_user.username

        return redirect("/secret")


    return render_template("login.html", form=form)


@app.get("/secret")
def display_secret_page():
    """Renders secret.html"""

    
    if session.get("username"):
        return render_template("secret.html")

    return render_template("login.html", form=LoginForm())
