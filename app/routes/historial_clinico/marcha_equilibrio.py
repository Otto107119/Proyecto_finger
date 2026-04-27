from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import MarchaEquilibrio
from app.forms.historial_clinico import MarchaEquilibrioForm

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/marcha-equilibrio", methods=["GET", "POST"])
@login_required
def historial_clinico_marcha_equilibrio(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    registro = MarchaEquilibrio.query.filter_by(historial_clinico_id=historial.id).first()

    if not registro:
        registro = MarchaEquilibrio(historial_clinico_id=historial.id)
        db.session.add(registro)
        db.session.commit()

    form = MarchaEquilibrioForm(obj=registro)

    if form.validate_on_submit():
        form.populate_obj(registro)
        db.session.commit()

        flash("Marcha y equilibrio guardado correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_marcha_equilibrio",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    return render_template(
        "historial_clinico/marcha_equilibrio.html",
        paciente=paciente,
        historial=historial,
        form=form,
        registro=registro
    )