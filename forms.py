from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, Optional, Email, Length, EqualTo


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


class TaskForm(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    due_date = DateField("Due Date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Add")


class EditTaskForm(FlaskForm):
    edit_title = StringField("Edit Title", validators=[DataRequired()])
    edit_due_date = DateField(
        "Edit Due Date", validators=[Optional()], format="%Y-%m-%d"
    )
    submit = SubmitField("Save")


class EditProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update Profile")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("confirm_new_password", message="Passwords must match"),
        ],
    )
    confirm_new_password = PasswordField(
        "Confirm New Password", validators=[DataRequired()]
    )
    submit = SubmitField("Change Password")
