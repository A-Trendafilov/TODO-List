from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Password")
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sing Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sing In!")
