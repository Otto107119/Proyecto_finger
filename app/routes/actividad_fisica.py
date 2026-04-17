from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Paciente, ActividadFisica
from app.forms import ActividadFisicaForm

actividad_fisica_bp = Blueprint(
    "actividad_fisica",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/actividad-fisica"
)


@actividad_fisica_bp.route("")
@login_required
def actividad_fisica_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    actividades = ActividadFisica.query.filter_by(
        paciente_id=paciente.id
    ).order_by(ActividadFisica.fecha.desc()).all()

    return render_template(
        "actividad_fisica/lista.html",
        paciente=paciente,
        actividades=actividades
    )


@actividad_fisica_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def actividad_fisica_nuevo(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadFisicaForm()

    if form.validate_on_submit():
        actividad = ActividadFisica(
            tipo=form.tipo.data,
            duracion_min=form.duracion_min.data,
            observaciones=form.observaciones.data,
            paciente_id=paciente.id,
            usuario_id=current_user.id
        )
        db.session.add(actividad)
        db.session.commit()

        flash("Actividad física registrada correctamente.", "success")
        return redirect(url_for("actividad_fisica.actividad_fisica_lista", paciente_id=paciente.id))

    return render_template(
        "actividad_fisica/nuevo.html",
        paciente=paciente,
        form=form
    )