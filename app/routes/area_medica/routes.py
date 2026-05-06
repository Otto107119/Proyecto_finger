from flask import Blueprint, render_template, redirect, url_for, flash, abort, send_file
from flask_login import login_required, current_user
from datetime import date

from app import db
from app.models import Paciente
from app.models.area_medica import AreaMedica
from app.forms.area_medica import AreaMedicaForm

from app.routes.area_medica.pdf import generar_pdf_area_medica_bytes
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors

from app.utils.permisos import (
    puede_ver_area,
    puede_crear_area,
    puede_editar_area,
    puede_eliminar_area,
    puede_descargar_pdf_area
)


area_medica_bp = Blueprint(
    "area_medica",
    __name__,
    url_prefix="/area-medica"
)

AREA = "area_medica"


def interpretar_riesgo(porcentaje):
    if porcentaje is None:
        return "No calculado"

    if porcentaje < 10:
        return "Riesgo bajo"
    elif porcentaje <= 20:
        return "Riesgo moderado"
    elif porcentaje > 30:
        return "Riesgo alto"
    else:
        return "Riesgo intermedio"


def calcular_edad(fecha_nacimiento):
    if not fecha_nacimiento:
        return None

    hoy = date.today()

    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )


@area_medica_bp.route("/paciente/<int:paciente_id>")
@login_required
def index(paciente_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)

    paciente = Paciente.query.get_or_404(paciente_id)

    registros = AreaMedica.query.filter_by(
        paciente_id=paciente.id
    ).order_by(
        AreaMedica.fecha_registro.desc()
    ).all()

    return render_template(
        "area_medica/index.html",
        paciente=paciente,
        registros=registros,
        puede_crear=puede_crear_area(current_user, AREA),
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
    )


@area_medica_bp.route("/paciente/<int:paciente_id>/nueva", methods=["GET", "POST"])
@login_required
def nueva(paciente_id):
    if not puede_crear_area(current_user, AREA):
        abort(403)

    paciente = Paciente.query.get_or_404(paciente_id)
    form = AreaMedicaForm()

    if form.validate_on_submit():
        registro = AreaMedica(
            paciente_id=paciente.id,

            sexo=paciente.genero,
            edad=calcular_edad(paciente.fecha_nacimiento),
            presion_sistolica=form.presion_sistolica.data,

            tratamiento_hipertension=form.tratamiento_hipertension.data,
            fumador=form.fumador.data,
            diabetico=form.diabetico.data,

            hdl=form.hdl.data,
            colesterol=form.colesterol.data,

            edad_corazon=form.edad_corazon.data,
            porcentaje_riesgo=form.porcentaje_riesgo.data,
            interpretacion_riesgo=interpretar_riesgo(form.porcentaje_riesgo.data),

            colesterol_total=form.colesterol_total.data,
            colesterol_ldl=form.colesterol_ldl.data,
            colesterol_hdl=form.colesterol_hdl.data,
            trigliceridos=form.trigliceridos.data,

            glucosa_capilar=form.glucosa_capilar.data,
        )

        db.session.add(registro)
        db.session.commit()

        flash("Área médica guardada correctamente.", "success")
        return redirect(url_for("area_medica.detalle", registro_id=registro.id))

    return render_template(
        "area_medica/form.html",
        form=form,
        paciente=paciente,
        modo="crear",
        edad_paciente=calcular_edad(paciente.fecha_nacimiento)
    )


@area_medica_bp.route("/<int:registro_id>")
@login_required
def detalle(registro_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)

    registro = AreaMedica.query.get_or_404(registro_id)

    return render_template(
        "area_medica/detalle.html",
        registro=registro,
        paciente=registro.paciente,
        puede_editar=puede_editar_area(current_user, AREA),
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
    )


@area_medica_bp.route("/<int:registro_id>/editar", methods=["GET", "POST"])
@login_required
def editar(registro_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)

    registro = AreaMedica.query.get_or_404(registro_id)
    paciente = registro.paciente

    form = AreaMedicaForm(obj=registro)

    if form.validate_on_submit():
        registro.presion_sistolica = form.presion_sistolica.data
        registro.tratamiento_hipertension = form.tratamiento_hipertension.data
        registro.fumador = form.fumador.data
        registro.diabetico = form.diabetico.data

        registro.hdl = form.hdl.data
        registro.colesterol = form.colesterol.data

        registro.edad_corazon = form.edad_corazon.data
        registro.porcentaje_riesgo = form.porcentaje_riesgo.data
        registro.interpretacion_riesgo = interpretar_riesgo(form.porcentaje_riesgo.data)

        registro.colesterol_total = form.colesterol_total.data
        registro.colesterol_ldl = form.colesterol_ldl.data
        registro.colesterol_hdl = form.colesterol_hdl.data
        registro.trigliceridos = form.trigliceridos.data

        registro.glucosa_capilar = form.glucosa_capilar.data

        db.session.commit()

        flash("Área médica actualizada correctamente.", "success")
        return redirect(url_for("area_medica.detalle", registro_id=registro.id))

    return render_template(
        "area_medica/form.html",
        form=form,
        paciente=paciente,
        registro=registro,
        modo="editar",
        edad_paciente=registro.edad
    )

@area_medica_bp.route("/<int:registro_id>/eliminar", methods=["POST"])
@login_required
def eliminar(registro_id):
    if not puede_eliminar_area(current_user, AREA):
        abort(403)

    registro = AreaMedica.query.get_or_404(registro_id)
    paciente_id = registro.paciente_id

    db.session.delete(registro)
    db.session.commit()

    flash("Registro de área médica eliminado correctamente.", "success")
    return redirect(url_for("area_medica.index", paciente_id=paciente_id))

@area_medica_bp.route("/<int:registro_id>/pdf")
@login_required
def pdf(registro_id):
    if not puede_descargar_pdf_area(current_user, AREA):
        abort(403)

    registro = AreaMedica.query.get_or_404(registro_id)

    pdf_buffer = generar_pdf_area_medica_bytes(
        registro.paciente,
        registro
    )

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"area_medica_{registro.id}.pdf",
        mimetype="application/pdf"
    )