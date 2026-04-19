from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models import Usuario
from app.forms import RegistroForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("pacientes.pacientes_lista"))
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegistroForm()

    if form.validate_on_submit():
        existente = Usuario.query.filter_by(correo=form.correo.data).first()
        if existente:
            flash("Ese correo ya está registrado.", "danger")
            return redirect(url_for("auth.register"))

        nuevo = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            password=generate_password_hash(form.password.data),
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("Usuario registrado correctamente.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data).first()

        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("auth.index"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))