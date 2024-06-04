import os

from dotenv import load_dotenv
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_login import login_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash

from db_model import db, User
from forms import RegisterForm, LoginForm

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db.init_app(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# Uncomment on the 1st run to create the database.
# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    form = LoginForm()
    if form.validate_on_submit():
        if request.form["action"] == "login":
            result = db.session.execute(
                db.select(User).where(User.email == form.email.data)
            )
            user = result.scalar()
            if not user:
                flash("That email does not exist, please try again.")
                return redirect(url_for("login"))
            elif not check_password_hash(user.password, form.password.data):
                flash("Password incorrect, please try again.")
                return redirect(url_for("login"))
            else:
                login_user(user)
                return redirect(url_for("get_all_posts"))
        elif request.form["action"] == "register":
            return redirect(url_for("create_account"))

    return render_template(
        "index.html",
        form=form,
    )  # current_user=current_user)


@app.route("/crate-account")
def create_account():
    form = RegisterForm()
    if form.validate_on_submit():
        result = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        )
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("home"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8,
        )
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form, current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True)
