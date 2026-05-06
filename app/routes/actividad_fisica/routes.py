from flask import render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import login_required, current_user

from app import db
from app.models import Paciente
from app.models.actividad_fisica import ActividadFisica
from app.forms.actividad_fisica import ActividadFisicaForm
from app.routes.actividad_fisica import actividad_fisica_bp
from app.routes.actividad_fisica.pdf import generar_pdf_actividad_fisica_bytes

from app.utils.permisos import (
    puede_ver_area,
    puede_crear_area,
    puede_editar_area,
    puede_eliminar_area,
    puede_descargar_pdf_area
)

AREA = "actividad_fisica"

@actividad_fisica_bp.route("/<int:paciente_id>")
@login_required
def lista(paciente_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
    
    paciente = Paciente.query.get_or_404(paciente_id)
    evaluaciones = ActividadFisica.query.filter_by(
        paciente_id=paciente.id
    ).order_by(
        ActividadFisica.fecha.desc()
    ).all()

    return render_template(
        "actividad_fisica/lista.html",
        paciente=paciente,
        evaluaciones=evaluaciones,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA)
    )


@actividad_fisica_bp.route("/<int:paciente_id>/nuevo", methods=["GET", "POST"])
@login_required
def nuevo(paciente_id):
    if not puede_crear_area(current_user, AREA):
        
        flash("No tienes permiso para capturar actividad física.", "danger")
        return redirect(url_for("actividad_fisica.lista", paciente_id=paciente_id))

    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadFisicaForm()

    if form.validate_on_submit():
        evaluacion = ActividadFisica(
            paciente_id=paciente.id,
            sentarse_levantarse_30s=form.sentarse_levantarse_30s.data,
            dinamometro_kg=form.dinamometro_kg.data,
            tug_segundos=form.tug_segundos.data,
            equilibrio_unipodal_segundos=form.equilibrio_unipodal_segundos.data,
            caminata_6min_metros=form.caminata_6min_metros.data,
            velocidad_marcha_ms=form.velocidad_marcha_ms.data,
            sppb_equilibrio=form.sppb_equilibrio.data,
            sppb_velocidad_marcha=form.sppb_velocidad_marcha.data,
            sppb_fuerza_piernas=form.sppb_fuerza_piernas.data,
            notas=form.notas.data
        )

        evaluacion.calcular_resultados()

        db.session.add(evaluacion)
        db.session.commit()

        flash("Evaluación física guardada correctamente.", "success")
        return redirect(url_for("actividad_fisica.lista", paciente_id=paciente.id))

    return render_template(
        "actividad_fisica/formulario.html",
        form=form,
        paciente=paciente,
        titulo="Nueva evaluación física",
        accion="Guardar evaluación"
    )


@actividad_fisica_bp.route("/detalle/<int:evaluacion_id>")
@login_required
def detalle(evaluacion_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
    
    evaluacion = ActividadFisica.query.get_or_404(evaluacion_id)
    paciente = Paciente.query.get_or_404(evaluacion.paciente_id)

    return render_template(
        "actividad_fisica/detalle.html",
        evaluacion=evaluacion,
        paciente=paciente,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA)
    )


@actividad_fisica_bp.route("/editar/<int:evaluacion_id>", methods=["GET", "POST"])
@login_required
def editar(evaluacion_id):
    if not puede_editar_area(current_user, AREA):
        
        flash("No tienes permiso para editar esta evaluación.", "danger")
        return redirect(request.referrer or url_for("pacientes.pacientes_lista"))

    evaluacion = ActividadFisica.query.get_or_404(evaluacion_id)
    paciente = Paciente.query.get_or_404(evaluacion.paciente_id)

    form = ActividadFisicaForm(obj=evaluacion)

    if form.validate_on_submit():
        form.populate_obj(evaluacion)
        evaluacion.calcular_resultados()

        db.session.commit()

        flash("Evaluación física actualizada correctamente.", "success")
        return redirect(url_for("actividad_fisica.detalle", evaluacion_id=evaluacion.id))

    return render_template(
        "actividad_fisica/formulario.html",
        form=form,
        paciente=paciente,
        evaluacion=evaluacion,
        titulo="Editar evaluación física",
        accion="Actualizar evaluación"
    )


@actividad_fisica_bp.route("/eliminar/<int:evaluacion_id>", methods=["POST"])
@login_required
def eliminar(evaluacion_id):
    if not puede_eliminar_area(current_user, AREA):
        
        flash("No tienes permiso para eliminar esta evaluación.", "danger")
        return redirect(request.referrer or url_for("pacientes.pacientes_lista"))

    evaluacion = ActividadFisica.query.get_or_404(evaluacion_id)
    paciente_id = evaluacion.paciente_id

    db.session.delete(evaluacion)
    db.session.commit()

    flash("Evaluación física eliminada correctamente.", "success")
    return redirect(url_for("actividad_fisica.lista", paciente_id=paciente_id))

@actividad_fisica_bp.route("/pdf/<int:evaluacion_id>")
@login_required
def pdf(evaluacion_id):
    if not puede_descargar_pdf_area(current_user, AREA):
        abort(403)
    
    evaluacion = ActividadFisica.query.get_or_404(evaluacion_id)
    paciente = Paciente.query.get_or_404(evaluacion.paciente_id)

    pdf_buffer = generar_pdf_actividad_fisica_bytes(paciente, evaluacion)

    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"actividad_fisica_{paciente.id}_{evaluacion.id}.pdf"
    )