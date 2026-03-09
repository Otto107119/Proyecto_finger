from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from app.models import Usuario, Paciente, ActividadFisica, HistorialClinico
from app.forms import RegistroForm, LoginForm, PacienteForm, ActividadFisicaForm, HistorialClinicoForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import abort
from functools import wraps


def role_required(*roles):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if current_user.rol not in roles:
                abort(403)
            return func(*args, **kwargs)
        return wrapper
    return decorator


main = Blueprint('main', __name__)

@main.route("/")
@login_required
def index():
    return render_template("dashboard.html")

@main.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            password=hashed_password,
            rol="capturista"
            )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario registrado correctamente")
        return redirect(url_for("main.login"))
    return render_template("registro.html", form=form)

@main.route("/crear_usuario", methods=["GET", "POST"])
@role_required("admin")
def crear_usuario():
    form = RegistroForm()

    if form.validate_on_submit():
        from flask import request

        rol = request.form.get("rol")

        hashed_password = generate_password_hash(form.password.data)

        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            correo=form.correo.data,
            password=hashed_password,
            rol=rol
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash("Usuario creado por administrador")
        return redirect(url_for("main.index"))

    return render_template("crear_usuario.html", form=form)


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(correo=form.correo.data).first()
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            return redirect(url_for("main.index"))
        flash("Credenciales incorrectas")
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main.route("/pacientes")
@login_required
def pacientes_lista():
    pacientes = Paciente.query.order_by(Paciente.fecha_registro.desc()).all()
    return render_template("pacientes_lista.html", pacientes=pacientes)

@main.route("/pacientes/nuevo", methods=["GET", "POST"])
@login_required
def pacientes_nuevo():
    form = PacienteForm()

    if form.validate_on_submit():
        nuevo = Paciente(
            nombre=form.nombre.data,
            edad=form.edad.data,
            genero=form.genero.data,
            usuario_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Paciente registrado correctamente ✅")
        return redirect(url_for("main.pacientes_lista"))

    return render_template("pacientes_nuevo.html", form=form)

@main.route("/pacientes/<int:paciente_id>")
@login_required
def pacientes_detalle(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    return render_template("pacientes_detalle.html", paciente=paciente)

@main.route("/pacientes/<int:paciente_id>/actividad_fisica")
@login_required
def actividad_fisica_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    actividades = ActividadFisica.query.filter_by(paciente_id=paciente_id).order_by(ActividadFisica.fecha.desc()).all()
    return render_template("actividad_fisica_lista.html", paciente=paciente, actividades=actividades)

@main.route("/pacientes/<int:paciente_id>/actividad_fisica/nueva", methods=["GET", "POST"])
@role_required("admin", "capturista")
def actividad_fisica_nueva(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadFisicaForm()

    if form.validate_on_submit():
        nueva = ActividadFisica(
            tipo=form.tipo.data,
            duracion_min=form.duracion_min.data,
            observaciones=form.observaciones.data,
            paciente_id=paciente.id,
            usuario_id=current_user.id
        )
        db.session.add(nueva)
        db.session.commit()
        flash("Actividad física registrada ✅")
        return redirect(url_for("main.actividad_fisica_lista", paciente_id=paciente.id))

    return render_template("actividad_fisica_nueva.html", paciente=paciente, form=form)

@main.route("/actividad_fisica/<int:actividad_id>/editar", methods=["GET", "POST"])
@role_required("admin", "capturista")
def actividad_fisica_editar(actividad_id):
    actividad = ActividadFisica.query.get_or_404(actividad_id)

    # (opcional) si quieres que capturista SOLO edite lo suyo:
    if current_user.rol == "capturista" and actividad.usuario_id != current_user.id:
        abort(403)

    form = ActividadFisicaForm(obj=actividad)

    if form.validate_on_submit():
        actividad.tipo = form.tipo.data
        actividad.duracion_min = form.duracion_min.data
        actividad.observaciones = form.observaciones.data
        db.session.commit()
        flash("Actividad actualizada ✅")
        return redirect(url_for("main.actividad_fisica_lista", paciente_id=actividad.paciente_id))

    return render_template("actividad_fisica_editar.html", form=form, actividad=actividad)

@main.route("/actividad_fisica/<int:actividad_id>/eliminar", methods=["POST"])
@role_required("admin")
def actividad_fisica_eliminar(actividad_id):
    actividad = ActividadFisica.query.get_or_404(actividad_id)
    paciente_id = actividad.paciente_id
    db.session.delete(actividad)
    db.session.commit()
    flash("Actividad eliminada 🗑️")
    return redirect(url_for("main.actividad_fisica_lista", paciente_id=paciente_id))

@main.route("/pacientes/<int:paciente_id>/historial_clinico")
@login_required
def historial_clinico_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    historiales = HistorialClinico.query.filter_by(paciente_id=paciente_id).order_by(HistorialClinico.fecha.desc()).all()
    return render_template("historial_clinico_lista.html", paciente=paciente, historiales=historiales)

@main.route("/pacientes/<int:paciente_id>/historial_clinico/nuevo", methods=["GET", "POST"])
@role_required("admin", "gerontologia")
def historial_clinico_nuevo(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = HistorialClinicoForm()

    if form.validate_on_submit():
        nuevo = HistorialClinico(
            motivo_consulta=form.motivo_consulta.data,
            antecedentes_personales=form.antecedentes_personales.data,
            antecedentes_familiares=form.antecedentes_familiares.data,
            padecimientos_actuales=form.padecimientos_actuales.data,
            medicamentos=form.medicamentos.data,
            alergias=form.alergias.data,
            observaciones=form.observaciones.data,
            paciente_id=paciente.id,
            usuario_id=current_user.id
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Historial clínico registrado correctamente ✅")
        return redirect(url_for("main.historial_clinico_lista", paciente_id=paciente.id))

    return render_template("historial_clinico_nuevo.html", paciente=paciente, form=form)

@main.route("/historial_clinico/<int:historial_id>/editar", methods=["GET", "POST"])
@role_required("admin", "gerontologia")
def historial_clinico_editar(historial_id):
    historial = HistorialClinico.query.get_or_404(historial_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        historial.motivo_consulta = form.motivo_consulta.data
        historial.antecedentes_personales = form.antecedentes_personales.data
        historial.antecedentes_familiares = form.antecedentes_familiares.data
        historial.padecimientos_actuales = form.padecimientos_actuales.data
        historial.medicamentos = form.medicamentos.data
        historial.alergias = form.alergias.data
        historial.observaciones = form.observaciones.data

        db.session.commit()
        flash("Historial clínico actualizado correctamente ✅")
        return redirect(url_for("main.historial_clinico_lista", paciente_id=historial.paciente_id))

    return render_template("historial_clinico_editar.html", form=form, historial=historial)