from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import EstudioComplementario
from app.forms.historial_clinico import EstudioComplementarioForm

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


@historial_clinico_bp.route("/<int:historial_id>/estudios-complementarios")
@login_required
def historial_clinico_estudios_complementarios(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    estudios = EstudioComplementario.query.filter_by(
        historial_clinico_id=historial.id
    ).all()

    return render_template(
        "historial_clinico/estudios_complementarios.html",
        paciente=paciente,
        historial=historial,
        estudios=estudios
    )


@historial_clinico_bp.route("/<int:historial_id>/estudios-complementarios/agregar", methods=["GET", "POST"])
@login_required
def historial_clinico_estudios_complementarios_agregar(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    form = EstudioComplementarioForm()

    if form.validate_on_submit():
        nuevo = EstudioComplementario(
            historial_clinico_id=historial.id,
            estudio=form.estudio.data,
            resultado=form.resultado.data,
            tratamiento=form.tratamiento.data,
            fecha_estudio=form.fecha_estudio.data,
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("Estudio complementario agregado correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_estudios_complementarios",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    return render_template(
        "historial_clinico/estudio_complementario_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Agregar estudio complementario"
    )


@historial_clinico_bp.route("/<int:historial_id>/estudios-complementarios/<int:estudio_id>/editar", methods=["GET", "POST"])
@login_required
def historial_clinico_estudios_complementarios_editar(paciente_id, historial_id, estudio_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    estudio = EstudioComplementario.query.get_or_404(estudio_id)

    if estudio.historial_clinico_id != historial.id:
        flash("Registro no válido para este paciente.", "danger")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_estudios_complementarios",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    form = EstudioComplementarioForm(obj=estudio)

    if form.validate_on_submit():
        form.populate_obj(estudio)
        db.session.commit()

        flash("Estudio complementario actualizado correctamente.", "success")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_estudios_complementarios",
                paciente_id=paciente.id
            )
        )

    return render_template(
        "historial_clinico/estudio_complementario_form.html",
        paciente=paciente,
        historial=historial,
        form=form,
        titulo="Editar estudio complementario"
    )


@historial_clinico_bp.route("/<int:historial_id>/estudios-complementarios/<int:estudio_id>/eliminar", methods=["POST"])
@login_required
def historial_clinico_estudios_complementarios_eliminar(paciente_id, historial_id, estudio_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)
    estudio = EstudioComplementario.query.get_or_404(estudio_id)

    if estudio.historial_clinico_id != historial.id:
        flash("Registro no válido para este paciente.", "danger")
        return redirect(
            url_for(
                "historial_clinico.historial_clinico_estudios_complementarios",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        )

    db.session.delete(estudio)
    db.session.commit()

    flash("Estudio complementario eliminado correctamente.", "success")
    return redirect(
        url_for(
            "historial_clinico.historial_clinico_estudios_complementarios",
            paciente_id=paciente.id
        )
    )