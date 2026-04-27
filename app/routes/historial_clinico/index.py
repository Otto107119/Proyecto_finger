from datetime import datetime
from flask import render_template, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from app.utils.decorators import roles_requeridos

from app import db
from app.models import (
    Paciente,
    HistorialClinico,
    ParesCraneales,
    MarchaEquilibrio,
    APHF,
    APPResumen,
    APPPatologia,
    FactoresRiesgo,
    EstudioComplementario,
    VisitaEspecialista,
)

from . import historial_clinico_bp


def texto_lleno(valor):
    return valor is not None and str(valor).strip() != ""


def tiene_datos_generales(historial):
    return any([
        texto_lleno(historial.escolaridad),
        texto_lleno(historial.estado_civil),
        texto_lleno(historial.ocupacion_actual),
        texto_lleno(historial.motivo_consulta),
        historial.sabe_leer,
        historial.sabe_escribir,
    ])


def tiene_area_social(historial):
    return any([
        historial.tiene_hijos,
        texto_lleno(historial.vive_con),
        historial.pension,
        texto_lleno(historial.ingreso_familiar_mensual),
        texto_lleno(historial.pasa_dia_con),
    ])


def tiene_area_espiritual(historial):
    return any([
        texto_lleno(historial.sentido_vida),
        texto_lleno(historial.mision_vida),
        historial.miedo_morir,
        texto_lleno(historial.metas_vida),
    ])


def tiene_area_psicologica(historial):
    return any([
        texto_lleno(historial.episodios_positivos),
        texto_lleno(historial.estado_animo),
        historial.perdidas,
        historial.duelo,
        historial.estres,
    ])


def tiene_area_fisica(historial):
    return any([
        texto_lleno(historial.estado_general),
        texto_lleno(historial.biotipo),
        texto_lleno(historial.talla),
        texto_lleno(historial.peso),
        historial.actividad_fisica,
    ])


@historial_clinico_bp.route("/")
@login_required
@roles_requeridos("admin", "superadmin", "gerontologia", "capturista")
def historiales_clinicos_lista(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historiales = HistorialClinico.query.filter_by(
        paciente_id=paciente.id
    ).order_by(HistorialClinico.creado_en.desc()).all()

    return render_template(
        "historial_clinico/lista.html",
        paciente=paciente,
        historiales=historiales
    )


@historial_clinico_bp.route("/nuevo", methods=["POST"])
@login_required
def historial_clinico_nuevo(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    nuevo = HistorialClinico(
        paciente_id=paciente.id,
        fecha=datetime.utcnow().date(),
        estado="en_captura"
    )

    db.session.add(nuevo)
    db.session.commit()

    flash("Nuevo historial clínico creado correctamente.", "success")

    return redirect(
        url_for(
            "historial_clinico.historial_clinico_datos_generales",
            paciente_id=paciente.id,
            historial_id=nuevo.id
        )
    )


@historial_clinico_bp.route("/<int:historial_id>/panel")
@login_required
def historial_clinico_index(paciente_id, historial_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(
        id=historial_id,
        paciente_id=paciente.id
    ).first_or_404()

    pares_craneales = ParesCraneales.query.filter_by(historial_clinico_id=historial.id).first()
    marcha_equilibrio = MarchaEquilibrio.query.filter_by(historial_clinico_id=historial.id).first()
    aphf = APHF.query.filter_by(historial_clinico_id=historial.id).first()
    app_resumen = APPResumen.query.filter_by(historial_clinico_id=historial.id).first()
    app_patologias = APPPatologia.query.filter_by(historial_clinico_id=historial.id).all()
    factores_riesgo = FactoresRiesgo.query.filter_by(historial_clinico_id=historial.id).first()
    estudios = EstudioComplementario.query.filter_by(historial_clinico_id=historial.id).all()
    visitas = VisitaEspecialista.query.filter_by(historial_clinico_id=historial.id).all()

    modulos = [
        {
            "nombre": "Datos generales",
            "capturado": tiene_datos_generales(historial),
            "url": url_for(
                "historial_clinico.historial_clinico_datos_generales",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Área social",
            "capturado": tiene_area_social(historial),
            "url": url_for(
                "historial_clinico.historial_clinico_area_social",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Área espiritual",
            "capturado": tiene_area_espiritual(historial),
            "url": url_for(
                "historial_clinico.historial_clinico_area_espiritual",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Área psicológica",
            "capturado": tiene_area_psicologica(historial),
            "url": url_for(
                "historial_clinico.historial_clinico_area_psicologica",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Área física",
            "capturado": tiene_area_fisica(historial),
            "url": url_for(
                "historial_clinico.historial_clinico_area_fisica",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Pares craneales",
            "capturado": pares_craneales is not None,
            "url": url_for(
                "historial_clinico.historial_clinico_pares_craneales",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Marcha y equilibrio",
            "capturado": marcha_equilibrio is not None,
            "url": url_for(
                "historial_clinico.historial_clinico_marcha_equilibrio",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "A.P.H.F.",
            "capturado": aphf is not None,
            "url": url_for(
                "historial_clinico.historial_clinico_aphf",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "A.P.P.",
            "capturado": bool(app_resumen or app_patologias),
            "url": url_for(
                "historial_clinico.historial_clinico_app",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Factores de riesgo",
            "capturado": factores_riesgo is not None,
            "url": url_for(
                "historial_clinico.historial_clinico_factores_riesgo",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Estudios complementarios",
            "capturado": len(estudios) > 0,
            "url": url_for(
                "historial_clinico.historial_clinico_estudios_complementarios",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
        {
            "nombre": "Visitas a especialista",
            "capturado": len(visitas) > 0,
            "url": url_for(
                "historial_clinico.historial_clinico_visitas_especialista",
                paciente_id=paciente.id,
                historial_id=historial.id
            )
        },
    ]

    return render_template(
        "historial_clinico/index.html",
        paciente=paciente,
        historial=historial,
        modulos=modulos
    )


@historial_clinico_bp.route("/<int:historial_id>/eliminar", methods=["POST"])
@login_required
def historial_clinico_eliminar(paciente_id, historial_id):
    if current_user.rol not in ["admin", "superadmin"]:
        abort(403)

    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(
        id=historial_id,
        paciente_id=paciente.id
    ).first_or_404()

    db.session.delete(historial)
    db.session.commit()

    flash("Historial clínico eliminado correctamente.", "success")

    return redirect(
        url_for(
            "historial_clinico.historiales_clinicos_lista",
            paciente_id=paciente.id
        )
    )