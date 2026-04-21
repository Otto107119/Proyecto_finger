from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.forms.historial_clinico import DatosGeneralesForm
from . import historial_clinico_bp
from .utils import obtener_historial


@historial_clinico_bp.route("/datos-generales", methods=["GET", "POST"])
@login_required
def historial_clinico_datos_generales(paciente_id):
    paciente, historial = obtener_historial(paciente_id)
    form = DatosGeneralesForm(obj=historial)

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