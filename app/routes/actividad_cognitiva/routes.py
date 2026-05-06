from flask import Blueprint, render_template, redirect, url_for, flash, abort, send_file
from flask_login import login_required, current_user
from datetime import datetime
from io import BytesIO

from app.utils.permisos import (
    puede_ver_area,
    puede_crear_area,
    puede_editar_area,
    puede_eliminar_area,
    puede_descargar_pdf_area
)

from app import db
from app.models import Paciente
from app.models.actividad_cognitiva import ActividadCognitiva
from app.forms.actividad_cognitiva import ActividadCognitivaForm
from app.routes.actividad_cognitiva.calculos import calcular_estimaciones
from app.routes.actividad_cognitiva.utils import obtener_punto_corte, generar_resumen_clinico
from app.routes.actividad_cognitiva.pdf import generar_pdf_actividad_cognitiva_bytes

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


actividad_cognitiva_bp = Blueprint(
    "actividad_cognitiva",
    __name__,
    url_prefix="/actividad-cognitiva"
)

AREA = "actividad_cognitiva"

def obtener_edad_paciente(paciente):
    if hasattr(paciente, "edad") and paciente.edad is not None:
        return paciente.edad

    if hasattr(paciente, "fecha_nacimiento") and paciente.fecha_nacimiento:
        hoy = datetime.today().date()
        nacimiento = paciente.fecha_nacimiento
        return hoy.year - nacimiento.year - (
            (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day)
        )

    return None


@actividad_cognitiva_bp.route("/paciente/<int:paciente_id>")
@login_required
def detalle(paciente_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
        
    paciente = Paciente.query.get_or_404(paciente_id)

    registros = ActividadCognitiva.query.filter_by(
        paciente_id=paciente.id
    ).order_by(ActividadCognitiva.fecha_evaluacion.desc()).all()

    return render_template(
        "actividad_cognitiva/menu.html",
        paciente=paciente,
        registros=registros,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
        )


@actividad_cognitiva_bp.route("/consulta/<int:registro_id>")
@login_required
def ver_consulta(registro_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
        
    registro = ActividadCognitiva.query.get_or_404(registro_id)
    paciente = registro.paciente

    return render_template(
        "actividad_cognitiva/detalle.html",
        paciente=paciente,
        registro=registro,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
        )


@actividad_cognitiva_bp.route("/paciente/<int:paciente_id>/crear", methods=["GET", "POST"])
@login_required
def crear(paciente_id):
    if not puede_crear_area(current_user, AREA):
        abort(403)
        
    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadCognitivaForm()

    if form.validate_on_submit():
        registro = ActividadCognitiva(
            paciente_id=paciente.id,
            fecha_evaluacion=form.fecha_evaluacion.data,
            examinador=form.examinador.data,
            edad=obtener_edad_paciente(paciente),
            escolaridad_anios=form.escolaridad_anios.data,
            ocupacion=form.ocupacion.data,
            preferencia_manual=form.preferencia_manual.data,

            moca_total=form.moca_total.data,

            digitos_directos_total=form.digitos_directos_total.data,
            digitos_directos_longitud=form.digitos_directos_longitud.data,
            digitos_inversos_total=form.digitos_inversos_total.data,
            digitos_inversos_longitud=form.digitos_inversos_longitud.data,

            trail_a_tiempo=form.trail_a_tiempo.data,
            trail_a_errores=form.trail_a_errores.data,
            trail_a_lineas_correctas=form.trail_a_lineas_correctas.data,

            trail_b_tiempo=form.trail_b_tiempo.data,
            trail_b_errores=form.trail_b_errores.data,
            trail_b_lineas_correctas=form.trail_b_lineas_correctas.data,

            mint_32_total=form.mint_32_total.data,

            fluencia_p=form.fluencia_p.data,
            fluencia_m=form.fluencia_m.data,

            animales_total=form.animales_total.data,
            vegetales_total=form.vegetales_total.data,

            benson_inmediata=form.benson_inmediata.data,
            benson_diferida=form.benson_diferida.data,

            craft_ri_44=form.craft_ri_44.data,
            craft_ri_parafraseo_25=form.craft_ri_parafraseo_25.data,
            craft_rd_44=form.craft_rd_44.data,
            craft_rd_parafraseo_25=form.craft_rd_parafraseo_25.data,
        )

        calcular_estimaciones(registro)

        db.session.add(registro)
        db.session.commit()

        flash("Actividad cognitiva guardada correctamente.", "success")
        return redirect(url_for(
            "actividad_cognitiva.detalle",
            paciente_id=paciente.id
        ))

    return render_template(
        "actividad_cognitiva/formulario.html",
        form=form,
        paciente=paciente,
        edad_paciente=obtener_edad_paciente(paciente),
        modo="crear"
    )


@actividad_cognitiva_bp.route("/editar/<int:registro_id>", methods=["GET", "POST"])
@login_required
def editar(registro_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)
        
    registro = ActividadCognitiva.query.get_or_404(registro_id)
    paciente = registro.paciente

    if registro.finalizado and not puede_editar_area(current_user, AREA):
        flash("No tienes permiso para editar este apartado.", "warning")
        return redirect(url_for(
            "actividad_cognitiva.ver_consulta",
            registro_id=registro.id
        ))

    form = ActividadCognitivaForm(obj=registro)

    if form.validate_on_submit():
        form.populate_obj(registro)
        calcular_estimaciones(registro)
        db.session.commit()

        flash("Actividad cognitiva actualizada correctamente.", "success")
        return redirect(url_for(
            "actividad_cognitiva.detalle",
            paciente_id=paciente.id
        ))

    return render_template(
        "actividad_cognitiva/formulario.html",
        form=form,
        paciente=paciente,
        registro=registro,
        edad_paciente=registro.edad or obtener_edad_paciente(paciente),
        modo="editar"
    )


@actividad_cognitiva_bp.route("/finalizar/<int:registro_id>", methods=["POST"])
@login_required
def finalizar(registro_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)

    registro = ActividadCognitiva.query.get_or_404(registro_id)

    calcular_estimaciones(registro)
    registro.finalizado = True

    db.session.commit()

    flash("Actividad cognitiva finalizada correctamente.", "success")
    return redirect(url_for(
        "actividad_cognitiva.detalle",
        paciente_id=registro.paciente_id
    ))


@actividad_cognitiva_bp.route("/desbloquear/<int:registro_id>", methods=["POST"])
@login_required
def desbloquear(registro_id):
    if not puede_eliminar_area(current_user, AREA):
        abort(403)

    registro = ActividadCognitiva.query.get_or_404(registro_id)
    registro.finalizado = False

    db.session.commit()

    flash("Actividad cognitiva desbloqueada para edición.", "success")
    return redirect(url_for(
        "actividad_cognitiva.detalle",
        paciente_id=registro.paciente_id
    ))


@actividad_cognitiva_bp.route("/eliminar/<int:registro_id>", methods=["POST"])
@login_required
def eliminar(registro_id):
    if not puede_eliminar_area(current_user, AREA):
        abort(403)

    registro = ActividadCognitiva.query.get_or_404(registro_id)
    paciente_id = registro.paciente_id

    db.session.delete(registro)
    db.session.commit()

    flash("Actividad cognitiva eliminada correctamente.", "success")
    return redirect(url_for(
        "actividad_cognitiva.detalle",
        paciente_id=paciente_id
    ))


@actividad_cognitiva_bp.route("/<int:consulta_id>/pdf")
@login_required
def pdf(consulta_id):
    if not puede_descargar_pdf_area(current_user, AREA):
        abort(403)

    consulta = ActividadCognitiva.query.get_or_404(consulta_id)

    pdf_buffer = generar_pdf_actividad_cognitiva_bytes(consulta)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"actividad_cognitiva_{consulta.id}.pdf",
        mimetype="application/pdf"
    )