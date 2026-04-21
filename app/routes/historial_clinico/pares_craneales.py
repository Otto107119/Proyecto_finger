from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import ParesCraneales
from app.forms.historial_clinico import ParesCranealesForm
from . import historial_clinico_bp
from .utils import obtener_historial


@historial_clinico_bp.route("/pares-craneales", methods=["GET", "POST"])
@login_required
def historial_clinico_pares_craneales(paciente_id):
    paciente, historial = obtener_historial(paciente_id)

    registro = ParesCraneales.query.filter_by(historial_clinico_id=historial.id).first()
    if not registro:
        registro = ParesCraneales(historial_clinico_id=historial.id)
        db.session.add(registro)
        db.session.commit()

    form = ParesCranealesForm(obj=registro)

    if form.validate_on_submit():
        form.populate_obj(registro)
        db.session.commit()
        flash("Pares craneales guardados correctamente.", "success")
        return redirect(
            url_for("historial_clinico.historial_clinico_pares_craneales", paciente_id=paciente.id)
        )

    return render_template(
        "historial_clinico/pares_craneales.html",
        paciente=paciente,
        historial=historial,
        form=form,
        registro=registro
    )