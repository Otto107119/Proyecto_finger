from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import Paciente, HistorialClinico
from app.forms import HistorialClinicoForm
from . import main

historial_clinico_bp = Blueprint(
    "historial_clinico",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/historial-clinico"
)


def obtener_historial(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(paciente_id=paciente.id).first()
    if not historial:
        historial = HistorialClinico(paciente_id=paciente.id)
        db.session.add(historial)
        db.session.commit()

    return paciente, historial


@historial_clinico_bp.route("/datos-generales", methods=["GET", "POST"])
@login_required
def historial_clinico_datos_generales(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Datos generales guardados correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_social", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/datos_generales.html",
        paciente=paciente,
        historial=historial,
        form=form
    )


@historial_clinico_bp.route("/area-social", methods=["GET", "POST"])
@login_required
def historial_clinico_area_social(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área social guardada correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_espiritual", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/area_social.html",
        paciente=paciente,
        historial=historial,
        form=form
    )


@historial_clinico_bp.route("/area-espiritual", methods=["GET", "POST"])
@login_required
def historial_clinico_area_espiritual(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área espiritual guardada correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_psicologica", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/area_espiritual.html",
        paciente=paciente,
        historial=historial,
        form=form
    )


@historial_clinico_bp.route("/area-psicologica", methods=["GET", "POST"])
@login_required
def historial_clinico_area_psicologica(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área psicológica guardada correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_psicologica", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/area_psicologica.html",
        paciente=paciente,
        historial=historial,
        form=form
    )


@historial_clinico_bp.route("/area-fisica", methods=["GET", "POST"])
@login_required
def historial_clinico_area_fisica(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = HistorialClinicoForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área física guardada correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_fisica", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/area_fisica.html",
        paciente=paciente,
        historial=historial,
        form=form
    )