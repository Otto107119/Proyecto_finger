from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user

from app import db
from app.models import Paciente
from app.forms import PacienteForm

pacientes_bp = Blueprint("pacientes", __name__, url_prefix="/pacientes")


@pacientes_bp.route("")
@login_required
def pacientes_lista():
    pacientes = Paciente.query.order_by(
    Paciente.registro_interno.asc().nullslast(),
    Paciente.nombre.asc()
    ).all()
    return render_template("pacientes/pacientes_lista.html", pacientes=pacientes)


@pacientes_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def pacientes_nuevo():
    form = PacienteForm()

    if form.validate_on_submit():
        paciente = Paciente(
            nombre=form.nombre.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            genero=form.genero.data,
            usuario_id=current_user.id
            
        )
        
        db.session.add(paciente)
        db.session.commit()

        flash("Paciente registrado correctamente.", "success")
        return redirect(url_for("pacientes.pacientes_lista"))

    return render_template("pacientes/pacientes_nuevo.html", form=form)


@pacientes_bp.route("/<int:paciente_id>")
@login_required
def pacientes_detalle(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    return render_template("pacientes/pacientes_detalle.html", paciente=paciente)


@pacientes_bp.route("/<int:paciente_id>/editar", methods=["GET", "POST"])
@login_required
def pacientes_editar(paciente_id):

    if current_user.rol != "superadmin":
        abort(403)

    paciente = Paciente.query.get_or_404(paciente_id)
    form = PacienteForm(obj=paciente)

    if form.validate_on_submit():
        registro_interno = request.form.get("registro_interno")

        if registro_interno:
            registro_interno = int(registro_interno)

            existente = Paciente.query.filter(
                Paciente.registro_interno == registro_interno,
                Paciente.id != paciente.id
            ).first()

            if existente:
                flash("Ese Registro Interno ya está asignado a otro paciente.", "danger")
                return redirect(url_for("pacientes.pacientes_editar", paciente_id=paciente.id))

            paciente.registro_interno = registro_interno
        else:
            paciente.registro_interno = None

        paciente.nombre = form.nombre.data
        paciente.fecha_nacimiento = form.fecha_nacimiento.data
        paciente.genero = form.genero.data

        db.session.commit()

        flash("Paciente actualizado correctamente.", "success")
        return redirect(url_for("pacientes.pacientes_lista"))

    return render_template("pacientes/pacientes_editar.html", form=form, paciente=paciente)


@pacientes_bp.route("/<int:paciente_id>/eliminar", methods=["POST"])
@login_required 
def pacientes_eliminar(paciente_id):

    if current_user.rol != "superadmin":
        abort(403)

    paciente = Paciente.query.get_or_404(paciente_id)

    db.session.delete(paciente)
    db.session.commit()

    flash("Paciente eliminado correctamente.", "success")

    return redirect(url_for("pacientes.pacientes_lista"))