from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.forms.historial_clinico import AreaSocialForm
from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/area-social", methods=["GET", "POST"])
@login_required
def historial_clinico_area_social(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    form = AreaSocialForm(obj=historial)

    if form.validate_on_submit():
        form.populate_obj(historial)
        db.session.commit()
        flash("Área social guardada correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_area_espiritual", 
            paciente_id=paciente.id,
            historial_id=historial.id)
        )

    return render_template(
        "historial_clinico/area_social.html",
        paciente=paciente,
        historial=historial,
        form=form
    )