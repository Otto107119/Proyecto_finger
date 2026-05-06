from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import login_required, current_user

from app import db
from app.models import Paciente
from app.models.actividad_nutricional import ActividadNutricional, RecordatorioNutricional, FrecuenciaGrasas
from app.forms.actividad_nutricional import ActividadNutricionalForm
from app.routes.actividad_nutricional.pdf import generar_pdf_actividad_nutricional_bytes

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)

from app.utils.permisos import (
    puede_ver_area,
    puede_crear_area,
    puede_editar_area,
    puede_eliminar_area,
    puede_descargar_pdf_area
)


actividad_nutricional_bp = Blueprint(
    "actividad_nutricional",
    __name__,
    url_prefix="/actividad-nutricional"
)

AREA = "actividad_nutricional"

def calcular_imc(peso, talla):
    if not peso or not talla:
        return None

    talla_metros = talla / 100

    if talla_metros <= 0:
        return None

    return round(peso / (talla_metros ** 2), 2)


def interpretar_calidad_dieta(puntaje):
    if puntaje >= 8:
        return "Buena calidad de la dieta"
    elif puntaje >= 5:
        return "Media calidad de la dieta"
    return "Mala calidad de la dieta"


def interpretar_mna(puntaje):
    if puntaje >= 12:
        return "Estado nutricional normal"
    elif puntaje >= 8:
        return "Riesgo de desnutrición"
    return "Desnutrición"


@actividad_nutricional_bp.route("/paciente/<int:paciente_id>/nueva", methods=["GET", "POST"])
@login_required
def nueva(paciente_id):
    if not puede_crear_area(current_user, AREA):
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    form = ActividadNutricionalForm()

    if form.validate_on_submit():

        calidad_dieta = sum([
            form.frutas_diarias.data,
            form.verduras_diarias.data,
            form.leguminosas.data,
            form.proteina_adecuada.data,
            form.cereales_integrales.data,
            form.limita_refrescos_jugos.data,
            form.limita_embutidos_procesados.data,
            form.agua_suficiente.data,
            form.grasas_saludables.data,
            form.mas_de_tres_comidas.data,
        ])

        valores_mna = [
            form.mna_ingesta.data,
            form.mna_perdida_peso.data,
            form.mna_movilidad.data,
            form.mna_estres.data,
            form.mna_neuropsicologicos.data,
            form.mna_imc.data,
        ]

        puntaje_mna = sum(int(valor) for valor in valores_mna if valor != "")

        imc = calcular_imc(form.peso.data, form.talla.data)

        actividad = ActividadNutricional(
            paciente_id=paciente.id,

            problemas_masticacion_deglucion=form.problemas_masticacion_deglucion.data,
            alergias_alimentos=form.alergias_alimentos.data,
            intolerancias_alimentos=form.intolerancias_alimentos.data,

            peso=form.peso.data,
            talla=form.talla.data,
            cintura=form.cintura.data,
            cadera=form.cadera.data,
            pantorrilla=form.pantorrilla.data,
            imc=imc,

            frutas_diarias=form.frutas_diarias.data,
            verduras_diarias=form.verduras_diarias.data,
            leguminosas=form.leguminosas.data,
            proteina_adecuada=form.proteina_adecuada.data,
            cereales_integrales=form.cereales_integrales.data,
            limita_refrescos_jugos=form.limita_refrescos_jugos.data,
            limita_embutidos_procesados=form.limita_embutidos_procesados.data,
            agua_suficiente=form.agua_suficiente.data,
            grasas_saludables=form.grasas_saludables.data,
            mas_de_tres_comidas=form.mas_de_tres_comidas.data,

            puntaje_calidad_dieta=calidad_dieta,
            interpretacion_calidad_dieta=interpretar_calidad_dieta(calidad_dieta),

            mna_ingesta=int(form.mna_ingesta.data) if form.mna_ingesta.data != "" else None,
            mna_perdida_peso=int(form.mna_perdida_peso.data) if form.mna_perdida_peso.data != "" else None,
            mna_movilidad=int(form.mna_movilidad.data) if form.mna_movilidad.data != "" else None,
            mna_estres=int(form.mna_estres.data) if form.mna_estres.data != "" else None,
            mna_neuropsicologicos=int(form.mna_neuropsicologicos.data) if form.mna_neuropsicologicos.data != "" else None,
            mna_imc=int(form.mna_imc.data) if form.mna_imc.data != "" else None,

            puntaje_mna=puntaje_mna,
            interpretacion_mna=interpretar_mna(puntaje_mna),

            dia_recordatorio=form.dia_recordatorio.data,
            observaciones=form.observaciones.data
        )

        db.session.add(actividad)
        db.session.flush()

        desayuno = RecordatorioNutricional(
            actividad_id=actividad.id,
            tiempo_comida="Desayuno",
            frutas=form.desayuno_frutas.data or 0,
            verduras=form.desayuno_verduras.data or 0,
            cereales=form.desayuno_cereales.data or 0,
            lacteos=form.desayuno_lacteos.data or 0,
            leguminosas=form.desayuno_leguminosas.data or 0,
            aoa=form.desayuno_aoa.data or 0,
            aceites_grasas=form.desayuno_aceites.data or 0,
            cafe=form.desayuno_cafe.data or 0,
            azucar=form.desayuno_azucar.data or 0
        )

        comida = RecordatorioNutricional(
            actividad_id=actividad.id,
            tiempo_comida="Comida",
            frutas=form.comida_frutas.data or 0,
            verduras=form.comida_verduras.data or 0,
            cereales=form.comida_cereales.data or 0,
            leguminosas=form.comida_leguminosas.data or 0,
            aoa=form.comida_aoa.data or 0,
            aceites_grasas=form.comida_aceites.data or 0
        )

        intermedio = RecordatorioNutricional(
            actividad_id=actividad.id,
            tiempo_comida="Intermedios",
            frutas=form.intermedio_frutas.data or 0,
            verduras=form.intermedio_verduras.data or 0,
            cereales=form.intermedio_cereales.data or 0,
            lacteos=form.intermedio_lacteos.data or 0,
            frutos_secos=form.intermedio_frutos_secos.data or 0
        )

        cena = RecordatorioNutricional(
            actividad_id=actividad.id,
            tiempo_comida="Cena",
            frutas=form.cena_frutas.data or 0,
            verduras=form.cena_verduras.data or 0,
            cereales=form.cena_cereales.data or 0,
            lacteos=form.cena_lacteos.data or 0,
            leguminosas=form.cena_leguminosas.data or 0,
            aoa=form.cena_aoa.data or 0,
            aceites_grasas=form.cena_aceites.data or 0
        )

        db.session.add(desayuno)
        db.session.add(comida)
        db.session.add(intermedio)
        db.session.add(cena)
        
        tipos_grasa = [
            "Aceite de soya",
            "Aceite de canola",
            "Aceite de maíz",
            "Aceite de oliva virgen extra",
            "Aguacate",
            "Frutos secos",
            "Manteca",
            "Mantequilla"
        ]

        for i, tipo in enumerate(tipos_grasa):
            frecuencia = request.form.get(f"frecuencia_grasa_{i}", "No utiliza")

            grasa = FrecuenciaGrasas(
                actividad_id=actividad.id,
                tipo_grasa=tipo,
                utiliza=frecuencia != "No utiliza",
                frecuencia=frecuencia
            )

            db.session.add(grasa)
        
        db.session.commit()

        flash("Actividad nutricional guardada correctamente.", "success")
        return redirect(url_for("actividad_nutricional.detalle", actividad_id=actividad.id))

    return render_template(
        "actividad_nutricional/form.html",
        form=form,
        paciente=paciente
    )


@actividad_nutricional_bp.route("/<int:actividad_id>")
@login_required
def detalle(actividad_id):
    actividad = ActividadNutricional.query.get_or_404(actividad_id)
    if not puede_ver_area(current_user, AREA):
        abort(403)
    return render_template(
        "actividad_nutricional/detalle.html",
        actividad=actividad,
        paciente=actividad.paciente,
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
        puede_editar=puede_editar_area(current_user, AREA),
    )


@actividad_nutricional_bp.route("/paciente/<int:paciente_id>")
@login_required
def index(paciente_id):
    if not puede_ver_area(current_user, AREA):
        abort(403)
    paciente = Paciente.query.get_or_404(paciente_id)
    actividades = ActividadNutricional.query.filter_by(
        paciente_id=paciente.id
    ).order_by(
        ActividadNutricional.fecha_registro.desc()
    ).all()

    return render_template(
        "actividad_nutricional/index.html",
        paciente=paciente,
        actividades=actividades,
        puede_eliminar=puede_eliminar_area(current_user, AREA),
        puede_pdf=puede_descargar_pdf_area(current_user, AREA),
        puede_editar=puede_editar_area(current_user, AREA),
    )

@actividad_nutricional_bp.route("/<int:actividad_id>/eliminar", methods=["POST"])
@login_required
def eliminar(actividad_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)
    actividad = ActividadNutricional.query.get_or_404(actividad_id)
    paciente_id = actividad.paciente_id

    RecordatorioNutricional.query.filter_by(actividad_id=actividad.id).delete()
    FrecuenciaGrasas.query.filter_by(actividad_id=actividad.id).delete()

    db.session.delete(actividad)
    db.session.commit()

    flash("Actividad nutricional eliminada correctamente.", "success")
    return redirect(url_for("actividad_nutricional.index", paciente_id=paciente_id))


@actividad_nutricional_bp.route("/<int:actividad_id>/editar", methods=["GET", "POST"])
@login_required
def editar(actividad_id):
    if not puede_editar_area(current_user, AREA):
        abort(403)
    actividad = ActividadNutricional.query.get_or_404(actividad_id)
    form = ActividadNutricionalForm(obj=actividad)

    if form.validate_on_submit():
        actividad.problemas_masticacion_deglucion = form.problemas_masticacion_deglucion.data
        actividad.alergias_alimentos = form.alergias_alimentos.data
        actividad.intolerancias_alimentos = form.intolerancias_alimentos.data

        actividad.peso = form.peso.data
        actividad.talla = form.talla.data
        actividad.cintura = form.cintura.data
        actividad.cadera = form.cadera.data
        actividad.pantorrilla = form.pantorrilla.data
        actividad.imc = calcular_imc(form.peso.data, form.talla.data)

        actividad.frutas_diarias = form.frutas_diarias.data
        actividad.verduras_diarias = form.verduras_diarias.data
        actividad.leguminosas = form.leguminosas.data
        actividad.proteina_adecuada = form.proteina_adecuada.data
        actividad.cereales_integrales = form.cereales_integrales.data
        actividad.limita_refrescos_jugos = form.limita_refrescos_jugos.data
        actividad.limita_embutidos_procesados = form.limita_embutidos_procesados.data
        actividad.agua_suficiente = form.agua_suficiente.data
        actividad.grasas_saludables = form.grasas_saludables.data
        actividad.mas_de_tres_comidas = form.mas_de_tres_comidas.data

        calidad_dieta = sum([
            form.frutas_diarias.data,
            form.verduras_diarias.data,
            form.leguminosas.data,
            form.proteina_adecuada.data,
            form.cereales_integrales.data,
            form.limita_refrescos_jugos.data,
            form.limita_embutidos_procesados.data,
            form.agua_suficiente.data,
            form.grasas_saludables.data,
            form.mas_de_tres_comidas.data,
        ])

        actividad.puntaje_calidad_dieta = calidad_dieta
        actividad.interpretacion_calidad_dieta = interpretar_calidad_dieta(calidad_dieta)

        valores_mna = [
            form.mna_ingesta.data,
            form.mna_perdida_peso.data,
            form.mna_movilidad.data,
            form.mna_estres.data,
            form.mna_neuropsicologicos.data,
            form.mna_imc.data,
        ]

        puntaje_mna = sum(int(valor) for valor in valores_mna if valor != "")

        actividad.mna_ingesta = int(form.mna_ingesta.data) if form.mna_ingesta.data != "" else None
        actividad.mna_perdida_peso = int(form.mna_perdida_peso.data) if form.mna_perdida_peso.data != "" else None
        actividad.mna_movilidad = int(form.mna_movilidad.data) if form.mna_movilidad.data != "" else None
        actividad.mna_estres = int(form.mna_estres.data) if form.mna_estres.data != "" else None
        actividad.mna_neuropsicologicos = int(form.mna_neuropsicologicos.data) if form.mna_neuropsicologicos.data != "" else None
        actividad.mna_imc = int(form.mna_imc.data) if form.mna_imc.data != "" else None

        actividad.puntaje_mna = puntaje_mna
        actividad.interpretacion_mna = interpretar_mna(puntaje_mna)

        actividad.dia_recordatorio = form.dia_recordatorio.data
        actividad.observaciones = form.observaciones.data

        tipos_grasa = [
            "Aceite de soya",
            "Aceite de canola",
            "Aceite de maíz",
            "Aceite de oliva virgen extra",
            "Aguacate",
            "Frutos secos",
            "Manteca",
            "Mantequilla"
        ]

        for i, tipo in enumerate(tipos_grasa):
            frecuencia = request.form.get(f"frecuencia_grasa_{i}", "No utiliza")

            grasa = FrecuenciaGrasas.query.filter_by(
                actividad_id=actividad.id,
                tipo_grasa=tipo
            ).first()

            if grasa:
                grasa.utiliza = frecuencia != "No utiliza"
                grasa.frecuencia = frecuencia
            else:
                grasa = FrecuenciaGrasas(
                    actividad_id=actividad.id,
                    tipo_grasa=tipo,
                    utiliza=frecuencia != "No utiliza",
                    frecuencia=frecuencia
                )
                db.session.add(grasa)

        db.session.commit()

        flash("Actividad nutricional actualizada correctamente.", "success")
        return redirect(url_for("actividad_nutricional.detalle", actividad_id=actividad.id))

    return render_template(
        "actividad_nutricional/form.html",
        form=form,
        paciente=actividad.paciente
    )

@actividad_nutricional_bp.route("/<int:actividad_id>/pdf")
@login_required
def pdf(actividad_id):
    if not puede_descargar_pdf_area(current_user, AREA):
        abort(403)

    actividad = ActividadNutricional.query.get_or_404(actividad_id)

    pdf_buffer = generar_pdf_actividad_nutricional_bytes(actividad)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"actividad_nutricional_{actividad.id}.pdf",
        mimetype="application/pdf"
    )