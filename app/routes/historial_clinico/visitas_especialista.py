from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import VisitaEspecialista
from app.forms.historial_clinico import VisitaEspecialistaForm

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/visitas-especialista")
@login_required
def historial_clinico_visitas_especialista(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    visitas = VisitaEspecialista.query.filter_by(
        historial_clinico_id=historial.id
    ).all()

    return render_template(
        "historial_clinico/visitas_especialista.html",
        paciente=paciente,
        historial=historial,
        visitas=visitas
    )


@historial_clinico_bp.route("/<int:historial_id>/visitas-especialista/agregar", methods=["GET", "POST"])
@login_required
def historial_clinico_visitas_especialista_agregar(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    form = VisitaEspecialistaForm()

    if form.validate_on_submit():
        nueva = VisitaEspecialista(
            historial_clinico_id=historial.id,
            fecha_visita=form.fecha_visita.data,
            especialista=form.especialista.data,
            motivo=form.motivo.data,
            tratamiento=form.tratamiento.data,
            estudios_requeridos=form.estudios_requeridos.data,
        )
        db.session.add(nueva)
        db.session.commit()

        flash("Visita a especialista agregada correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_visitas_especialista",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    return render_template(
        "historial_clinico/visita_especialista_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Agregar visita a especialista"
    )


@historial_clinico_bp.route("/<int:historial_id>/visitas-especialista/<int:visita_id>/editar", methods=["GET", "POST"])
@login_required
def historial_clinico_visitas_especialista_editar(paciente_id, historial_id, visita_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    visita = VisitaEspecialista.query.get_or_404(visita_id)

    if visita.historial_clinico_id != historial.id:
        flash("Registro no válido para este paciente.", "danger")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_visitas_especialista",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    form = VisitaEspecialistaForm(obj=visita)

    if form.validate_on_submit():
        form.populate_obj(visita)
        db.session.commit()

        flash("Visita a especialista actualizada correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_visitas_especialista",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    return render_template(
        "historial_clinico/visita_especialista_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Editar visita a especialista"
    )


@historial_clinico_bp.route("/<int:historial_id>/visitas-especialista/<int:visita_id>/eliminar", methods=["POST"])
@login_required
def historial_clinico_visitas_especialista_eliminar(paciente_id, historial_id, visita_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    visita = VisitaEspecialista.query.get_or_404(visita_id)

    if visita.historial_clinico_id != historial.id:
        flash("Registro no válido para este paciente.", "danger")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_visitas_especialista",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    db.session.delete(visita)
    db.session.commit()

    flash("Visita a especialista eliminada correctamente.", "success")
    return redirect(
        url_for(
            "historial_clinico.historial_clinico_visitas_especialista",
            paciente_id=paciente.id,
            historial_id=historial.id
        )
    )