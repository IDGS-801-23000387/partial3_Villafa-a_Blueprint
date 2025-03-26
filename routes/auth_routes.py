from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.models import db, User
from forms.auth_form import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("auth.index"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("Login/login.html", form=form)



@auth_bp.route("/index", methods=["GET", "POST"])
def index():
    

    return render_template("Login/index.html" )
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("El nombre de usuario ya está en uso", "danger")
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))

    return render_template("Login/registro.html", form=form)
