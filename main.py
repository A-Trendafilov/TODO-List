import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import (
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from db_model import db, User, Task
from forms import RegisterForm, LoginForm, TaskForm, EditForm

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Uncomment on the 1st run to create the database.
with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def home():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == login_form.email.data)
        )
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again or Sing Up!", "error")
            return redirect(url_for("home"))
        elif not check_password_hash(user.password, login_form.password.data):
            flash("Password incorrect, please try again.", "error")
            return redirect(url_for("home"))
        else:
            login_user(user)
            flash("You are successfully logged in.", "success")
            return redirect(url_for("tasks"))
    return render_template("index.html", form=login_form, current_user=current_user)


@app.route("/create-account", methods=["GET", "POST"])
def create_account():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == reg_form.email.data)
        )
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!", "error")
            return redirect(url_for("home"))

        hash_and_salted_password = generate_password_hash(
            reg_form.password.data,
            method="pbkdf2:sha256",
            salt_length=8,
        )
        new_user = User(
            email=reg_form.email.data,
            password=hash_and_salted_password,
            name=reg_form.name.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(
            f"{new_user.name} - Your account is created successfully! You are now logged in.",
            "success",
        )
        return redirect(url_for("tasks"))
    return render_template("register.html", form=reg_form, current_user=current_user)


@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    task_form = TaskForm()
    if task_form.validate_on_submit() and current_user.is_authenticated:
        new_task = Task(
            title=task_form.task.data,
            due_date=task_form.due_date.data,
            created_date=datetime.now(),
            author_id=current_user.id,
        )
        db.session.add(new_task)
        db.session.commit()
        flash(f"New tasks: {new_task.title}  - added successfully!", "success")
        return redirect(url_for("tasks"))

    if current_user.is_authenticated:
        result = db.session.execute(
            db.select(Task).where(Task.author_id == current_user.id)
        )
        user_tasks = result.scalars().all()
    else:
        user_tasks = []

    formatted_tasks = []
    for task in user_tasks:
        formatted_task = {
            "id": task.id,
            "title": task.title,
            "due_date": task.due_date.strftime("%d-%m-%Y") if task.due_date else None,
            "created_date": task.created_date.strftime("%d-%m-%Y"),
            "completed": task.completed,
            "author_id": task.author_id,
        }
        formatted_tasks.append(formatted_task)
    return render_template(
        "tasks.html", current_user=current_user, form=task_form, tasks=formatted_tasks
    )


@app.route("/tasks/delete/<int:task_id>")
@login_required
def delete_task(task_id):
    task_to_delete = db.get_or_404(Task, task_id)
    if task_to_delete.completed:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash(
            f"Completed task '{task_to_delete.title}' deleted successfully!", "success"
        )
        return redirect(url_for("completed_tasks"))
    else:
        db.session.delete(task_to_delete)
        db.session.commit()
        flash(f"Task '{task_to_delete.title}' deleted successfully!", "success")
        return redirect(url_for("tasks"))


@app.route("/tasks/complete/<int:task_id>")
@login_required
def complete_task(task_id):
    task_to_complete = db.get_or_404(Task, task_id)
    task_to_complete.completed = True
    task_to_complete.completed_date = datetime.now()
    db.session.commit()
    flash(f"Task: {task_to_complete.title} - is completed successfully!", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task_to_edit = db.get_or_404(Task, task_id)
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        task_to_edit.title = edit_form.edit_title.data
        task_to_edit.due_date = edit_form.edit_due_date.data
        db.session.commit()
        flash("Task updated successfully!", "success")
        return redirect(url_for("tasks"))
    return render_template("edit.html", form=edit_form, task=task_to_edit)


@app.route("/tasks/completed")
@login_required
def completed_tasks():
    result = db.session.execute(
        db.select(Task).where((Task.author_id == current_user.id) & Task.completed)
    )
    comp_tasks = result.scalars().all()
    formatted_completed_tasks = [
        {
            "id": task.id,
            "title": task.title,
            "due_date": task.due_date.strftime("%d-%m-%Y") if task.due_date else None,
            "created_date": task.created_date.strftime("%d-%m-%Y"),
            "completed_date": task.completed_date.strftime("%d-%m-%Y"),
        }
        for task in comp_tasks
    ]
    return render_template(
        "completed.html",
        current_user=current_user,
        completed_tasks=formatted_completed_tasks,
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are successfully logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
