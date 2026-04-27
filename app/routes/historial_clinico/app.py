from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.models import APPResumen, APPPatologia
from app.forms.historial_clinico import APPResumenForm, APPPatologiaForm

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/app", methods=["GET", "POST"])
@login_required
def historial_clinico_app(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    resumen = APPResumen.query.filter_by(historial_clinico_id=historial.id).first()
    if not resumen:
        resumen = APPResumen(historial_clinico_id=historial.id)
        db.session.add(resumen)
        db.session.commit()

    form = APPResumenForm(obj=resumen)
    patologias = APPPatologia.query.filter_by(historial_clinico_id=historial.id).all()

    if form.validate_on_submit():
        form.populate_obj(resumen)
        db.session.commit()
        flash("A.P.P. guardado correctamente.", "success")
        return redirect(url_for("historial_clinico.historial_clinico_app", 
        paciente_id=paciente.id,
        historial_id=historial.id))

    return render_template(
        "historial_clinico/app.html",
        paciente=paciente,
        historial=historial,
        form=form,
        resumen=resumen,
        patologias=patologias
    )


@historial_clinico_bp.route("/<int:historial_id>/app/agregar", methods=["GET", "POST"])
@login_required
def historial_clinico_app_agregar(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    form = APPPatologiaForm()

    if form.validate_on_submit():
        nueva = APPPatologia(
            historial_clinico_id=historial.id,
            patologia=form.patologia.data,
            hace_cuanto=form.hace_cuanto.data,
            diagnostico=form.diagnostico.data,
            farmaco=form.farmaco.data,
            dosis=form.dosis.data,
        )
        db.session.add(nueva)
        db.session.commit()

        flash("Antecedente agregado correctamente.", "success")
        return redirect(url_for("historial_clinico.historial_clinico_app", 
        paciente_id=paciente.id,
        historial_id=historial.id))

    return render_template(
        "historial_clinico/app_patologia_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Agregar antecedente patológico personal"
    )


@historial_clinico_bp.route("/<int:historial_id>/app/<int:patologia_id>/editar", methods=["GET", "POST"])
@login_required
def historial_clinico_app_editar(paciente_id, historial_id, patologia_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    patologia = APPPatologia.query.get_or_404(patologia_id)

    form = APPPatologiaForm(obj=patologia)

    if form.validate_on_submit():
        form.populate_obj(patologia)
        db.session.commit()

        flash("Antecedente actualizado correctamente.", "success")
        return redirect(url_for("historial_clinico.historial_clinico_app", 
        paciente_id=paciente.id,
        historial_id=historial.id))

    return render_template(
        "historial_clinico/app_patologia_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Editar antecedente patológico personal"
    )


@historial_clinico_bp.route("/<int:historial_id>/app/<int:patologia_id>/eliminar", methods=["POST"])
@login_required
def historial_clinico_app_eliminar(paciente_id, historial_id, patologia_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    patologia = APPPatologia.query.get_or_404(patologia_id)

    db.session.delete(patologia)
    db.session.commit()

    flash("Antecedente eliminado correctamente.", "success")
    return redirect(url_for("historial_clinico.historial_clinico_app", 
    paciente_id=paciente.id,
    historial_id=historial.id))