from datetime import datetime

from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from app import db
from app.models import (
    ParesCraneales,
    MarchaEquilibrio,
    APHF,
    APPResumen,
    APPPatologia,
    FactoresRiesgo,
    EstudioComplementario,
    VisitaEspecialista,
)
from app.utils.decorators import roles_requeridos

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


def texto_lleno(valor):
    return valor is not None and str(valor).strip() != ""


def seccion_datos_generales_completa(historial):
    return any([
        texto_lleno(historial.escolaridad),
        historial.sabe_leer,
        historial.sabe_escribir,
        texto_lleno(historial.estado_civil),
        texto_lleno(historial.ocupacion_actual),
        texto_lleno(historial.motivo_consulta),
    ])


def seccion_area_social_completa(historial):
    return any([
        historial.tiene_hijos,
        texto_lleno(historial.vive_con),
        historial.pension,
        texto_lleno(historial.ingreso_familiar_mensual),
        texto_lleno(historial.pasa_dia_con),
    ])


def seccion_area_espiritual_completa(historial):
    return any([
        texto_lleno(historial.sentido_vida),
        texto_lleno(historial.mision_vida),
        historial.miedo_morir,
        texto_lleno(historial.metas_vida),
    ])


def seccion_area_psicologica_completa(historial):
    return any([
        texto_lleno(historial.episodios_positivos),
        texto_lleno(historial.estado_animo),
        historial.perdidas,
        historial.duelo,
        historial.estres,
        texto_lleno(historial.comunicacion_verbal),
    ])


def seccion_area_fisica_completa(historial):
    return any([
        historial.incontinencia,
        texto_lleno(historial.estado_general),
        texto_lleno(historial.biotipo),
        texto_lleno(historial.talla),
        texto_lleno(historial.peso),
        historial.actividad_fisica,
    ])


def seccion_pares_craneales_completa(registro):
    if not registro:
        return False
    return any([
        registro.evaluados,
        registro.sin_alteraciones,
        texto_lleno(registro.alteraciones),
        texto_lleno(registro.observaciones_generales),
        registro.dentadura_postiza,
        texto_lleno(registro.piezas_perdidas),
    ])


def seccion_marcha_equilibrio_completa(registro):
    if not registro:
        return False
    return any([
        registro.cifosis,
        registro.lordosis,
        registro.escoliosis,
        registro.mareos,
        registro.sincope,
        registro.caidas,
        registro.fracturas,
        texto_lleno(registro.ayudas_tecnicas),
    ])


def seccion_aphf_completa(registro):
    if not registro:
        return False
    return any([
        registro.vive_padre,
        registro.vive_madre,
        texto_lleno(registro.padecimientos_padre),
        texto_lleno(registro.padecimientos_madre),
        registro.diabetes,
        registro.hipertension,
        texto_lleno(registro.observaciones),
    ])


def seccion_app_completa(resumen, patologias):
    return bool(resumen and any([
        texto_lleno(resumen.numero_embarazos),
        texto_lleno(resumen.farmacos_no_especificados),
        texto_lleno(resumen.medicina_alterna),
    ]) or patologias)


def seccion_factores_riesgo_completa(registro):
    if not registro:
        return False
    return any([
        registro.alcohol,
        registro.tabaco,
        registro.drogas,
        registro.vida_sexual_activa,
        texto_lleno(registro.observaciones),
    ])


def seccion_estudios_complementarios_completa(estudios):
    return len(estudios) > 0


def seccion_visitas_especialista_completa(visitas):
    return len(visitas) > 0


@historial_clinico_bp.route("/<int:historial_id>/resumen")
@login_required
@roles_requeridos("admin", "superadmin", "gerontologia", "capturista")
def historial_clinico_resumen(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    pares_craneales = ParesCraneales.query.filter_by(historial_clinico_id=historial.id).first()
    marcha_equilibrio = MarchaEquilibrio.query.filter_by(historial_clinico_id=historial.id).first()
    aphf = APHF.query.filter_by(historial_clinico_id=historial.id).first()
    app_resumen = APPResumen.query.filter_by(historial_clinico_id=historial.id).first()
    app_patologias = APPPatologia.query.filter_by(historial_clinico_id=historial.id).all()
    factores_riesgo = FactoresRiesgo.query.filter_by(historial_clinico_id=historial.id).first()
    estudios = EstudioComplementario.query.filter_by(historial_clinico_id=historial.id).all()
    visitas = VisitaEspecialista.query.filter_by(historial_clinico_id=historial.id).all()

    checklist = [
        ("Datos generales", seccion_datos_generales_completa(historial)),
        ("Área social", seccion_area_social_completa(historial)),
        ("Área espiritual", seccion_area_espiritual_completa(historial)),
        ("Área psicológica", seccion_area_psicologica_completa(historial)),
        ("Área física", seccion_area_fisica_completa(historial)),
        ("Pares craneales", seccion_pares_craneales_completa(pares_craneales)),
        ("Marcha y equilibrio", seccion_marcha_equilibrio_completa(marcha_equilibrio)),
        ("A.P.H.F.", seccion_aphf_completa(aphf)),
        ("A.P.P.", seccion_app_completa(app_resumen, app_patologias)),
        ("Factores de riesgo", seccion_factores_riesgo_completa(factores_riesgo)),
        ("Estudios complementarios", seccion_estudios_complementarios_completa(estudios)),
        ("Visitas a especialista", seccion_visitas_especialista_completa(visitas)),
    ]

    completas = sum(1 for _, ok in checklist if ok)
    total = len(checklist)
    progreso = int((completas / total) * 100) if total else 0

    return render_template(
        "historial_clinico/resumen.html",
        paciente=paciente,
        historial=historial,
        checklist=checklist,
        progreso=progreso,
        pares_craneales=pares_craneales,
        marcha_equilibrio=marcha_equilibrio,
        aphf=aphf,
        app_resumen=app_resumen,
        app_patologias=app_patologias,
        factores_riesgo=factores_riesgo,
        estudios=estudios,
        visitas=visitas,
    )


@historial_clinico_bp.route("/<int:historial_id>/finalizar", methods=["POST"])
@login_required
@roles_requeridos("admin", "superadmin", "gerontologia", "capturista")
def historial_clinico_finalizar(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    historial.estado = "finalizado"

    db.session.commit()

    flash("Historial finalizado correctamente.", "success")

    return redirect(
        url_for(
            "historial_clinico.historiales_clinicos_lista",
            paciente_id=paciente.id
        )
    )