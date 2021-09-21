from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username: ", validators=[
                           InputRequired(), Length(min=6, max=20)])
    # this password is not hashed
    password = PasswordField("Password: ", validators=[InputRequired()])
    first_name = StringField("First Name: ", validators=[
                             InputRequired(), Length(min=1, max=30)])
    last_name = StringField("Last Name: ", validators=[
                            InputRequired(), Length(min=1, max=30)])
    email = StringField("Email: ", validators=[
        InputRequired(), Length(min=1, max=30), Email()])


class LoginForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username: ", validators=[
                           InputRequired(), Length(min=6, max=20)])
    password = PasswordField("Password: ", validators=[InputRequired()])
