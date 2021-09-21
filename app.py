from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm, LogoutForm
from sqlalchemy import exc

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
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(
            username, password, first_name, last_name, email)

        try:
            db.session.add(new_user)
            db.session.commit()

            session["username"] = username

            return redirect(f"/user/{username}")

        except exc.IntegrityError:
            flash("This username or email already exists")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def process_login_form():
    # TODO:change view function name and update docstring
    """
    Process login form, saves login user to session
    """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data

        curr_user = User.authenticate(username, form.password.data)

        if not(curr_user):
            return render_template("login.html", form=form)

        session["username"] = curr_user.username

        return redirect(f"/user/{curr_user.username}")

    return render_template("login.html", form=form)


@app.get("/user/<username>")
def display_user_details(username):
    """Checks if user is logged in.
    If user is not logged in, render login form.
    If user tries to access a different user's details, redirect to their own details.
    If user is logged in user, show user details.
    """

    saved_username = session.get("username")

    if not saved_username:
        flash("Please log in to see user details~")
        return redirect("/login", form=LoginForm())

    if saved_username != username:
        return redirect(f"/user/{saved_username}")

    user = User.query.get_or_404(username)
    return render_template("user_details.html", user=user, form=LogoutForm())


@app.post("/logout")
def user_logout():
    """Logs out current user and clears session info"""
    # Make instance of form, use validate on submit so that we have CSRF protection
    if not session.get("username"):
        return redirect("/login")

    session.pop("username", None)
    return redirect("/")
