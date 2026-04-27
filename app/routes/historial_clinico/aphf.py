from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import APHF
from app.forms.historial_clinico import APHFForm

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/aphf", methods=["GET", "POST"])
@login_required
def historial_clinico_aphf(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    registro = APHF.query.filter_by(historial_clinico_id=historial.id).first()

    if not registro:
        registro = APHF(historial_clinico_id=historial.id)
        db.session.add(registro)
        db.session.commit()

    form = APHFForm(obj=registro)

    if form.validate_on_submit():
        form.populate_obj(registro)
        db.session.commit()

        flash("A.P.H.F. guardado correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_aphf",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    return render_template(
        "historial_clinico/aphf.html",
        paciente=paciente,
        historial=historial,
        form=form,
        registro=registro
    )