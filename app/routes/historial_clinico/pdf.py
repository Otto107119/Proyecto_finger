from io import BytesIO
from flask import send_file
from flask_login import login_required

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

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

from . import historial_clinico_bp
from .utils import obtener_historial_por_id


def v(valor):
    return str(valor) if valor not in [None, ""] else "—"


def sn(valor):
    return "[X] Sí   [ ] No" if valor else "[ ] Sí   [X] No"


def p(texto, style):
    return Paragraph(str(texto).replace("\n", "<br/>"), style)


def titulo_seccion(texto, styles):
    return [
        Spacer(1, 8),
        Paragraph(texto, styles["SectionTitle"]),
        Spacer(1, 4)
    ]


def tabla_kv(datos, styles, col_widths=None):
    contenido = []
    fila = []

    for etiqueta, valor in datos:
        fila.append(p(f"<b>{etiqueta}:</b> {v(valor)}", styles["Small"]))
        if len(fila) == 2:
            contenido.append(fila)
            fila = []

    if fila:
        fila.append("")
        contenido.append(fila)

    tabla = Table(contenido, colWidths=col_widths or [8.2 * cm, 8.2 * cm])
    tabla.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return tabla


def tabla_lista(encabezados, filas, styles):
    data = [[p(f"<b>{h}</b>", styles["Small"]) for h in encabezados]]

    if filas:
        for fila in filas:
            data.append([p(v(celda), styles["Small"]) for celda in fila])
    else:
        data.append([p("Sin registros", styles["Small"])] + [""] * (len(encabezados) - 1))

    tabla = Table(data, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.4, colors.grey),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e9ecef")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return tabla


def bloque_texto(titulo, texto, styles):
    return [
        Paragraph(f"<b>{titulo}</b>", styles["Small"]),
        Table(
            [[p(v(texto), styles["Small"])]],
            colWidths=[16.4 * cm],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ])
        ),
        Spacer(1, 6)
    ]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(20 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def generar_pdf_historial_bytes(paciente, historial):

    pares = ParesCraneales.query.filter_by(historial_clinico_id=historial.id).first()
    marcha = MarchaEquilibrio.query.filter_by(historial_clinico_id=historial.id).first()
    aphf = APHF.query.filter_by(historial_clinico_id=historial.id).first()
    app_resumen = APPResumen.query.filter_by(historial_clinico_id=historial.id).first()
    app_patologias = APPPatologia.query.filter_by(historial_clinico_id=historial.id).all()
    factores = FactoresRiesgo.query.filter_by(historial_clinico_id=historial.id).first()
    estudios = EstudioComplementario.query.filter_by(historial_clinico_id=historial.id).all()
    visitas = VisitaEspecialista.query.filter_by(historial_clinico_id=historial.id).all()

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCenter",
        parent=styles["Title"],
        alignment=1,
        fontSize=16,
        leading=20,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        textColor=colors.white,
        backColor=colors.HexColor("#0d6efd"),
        borderPadding=5,
        spaceBefore=8,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name="Small",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11
    ))

    story = []

    story.append(Paragraph("HISTORIAL CLÍNICO", styles["TitleCenter"]))
    story.append(tabla_kv([
        ("Fecha", historial.fecha),
        ("Estado", historial.estado),
        ("Nombre del participante", getattr(paciente, "nombre", "")),
        ("Edad", getattr(paciente, "edad", "")),
        ("Fecha de nacimiento", getattr(paciente, "fecha_nacimiento", "")),
        ("Género", getattr(paciente, "genero", "")),
        ("Contacto 1", f"{v(historial.contacto_nombre)} / {v(historial.contacto_telefono)}"),
        ("Contacto 2", f"{v(historial.contacto_nombre_2)} / {v(historial.contacto_telefono_2)}"),
        ("Fuente de valoración", historial.fuente_valoracion),
        ("", ""),
    ], styles))
    story.append(Spacer(1, 8))

    story += titulo_seccion("DATOS GENERALES", styles)
    story.append(tabla_kv([
        ("Escolaridad", historial.escolaridad),
        ("Sabe leer", sn(historial.sabe_leer)),
        ("Sabe escribir", sn(historial.sabe_escribir)),
        ("Estado civil", historial.estado_civil),
        ("Ocupación anterior", historial.ocupacion_anterior),
        ("Ocupación actual", historial.ocupacion_actual),
        ("Domicilio origen", historial.domicilio_origen),
        ("Domicilio actual", historial.domicilio_actual),
        ("Núcleo procedencia", historial.nucleo_procedencia),
        ("Vivienda", historial.vivienda),
        ("Servicios", f"Luz: {sn(historial.servicio_luz)} | Agua: {sn(historial.servicio_agua)} | Tel: {sn(historial.servicio_tel)} | Internet: {sn(historial.servicio_internet)}"),
        ("", ""),
    ], styles))
    story += bloque_texto("Motivo de consulta", historial.motivo_consulta, styles)

    story += titulo_seccion("ÁREA SOCIAL", styles)
    story.append(tabla_kv([
        ("Tiene hijos", sn(historial.tiene_hijos)),
        ("Hijas / Hijos", f"Mujeres: {v(historial.hijas_mujeres)} | Hombres: {v(historial.hijos_hombres)}"),
        ("Vive con", historial.vive_con),
        ("Pensión", sn(historial.pension)),
        ("Cuál pensión", historial.pension_cual),
        ("Ingreso familiar mensual", historial.ingreso_familiar_mensual),
        ("Redes de apoyo", f"Amigos: {sn(historial.red_apoyo_amigos)} | Familia: {sn(historial.red_apoyo_familia)} | Vecinos: {sn(historial.red_apoyo_vecinos)} | Nietos: {sn(historial.red_apoyo_nietos)}"),
        ("Acude taller", f"{sn(historial.acude_taller)} | {v(historial.taller_cual)}"),
        ("Frecuencia sale por semana", historial.frecuencia_sale_semana),
        ("Con quién sale", historial.con_quien_sale),
        ("Cuidador", f"{sn(historial.cuidador)} | {v(historial.cuidador_quien)}"),
        ("Cuidador remunerado", sn(historial.cuidador_remunerado)),
        ("Antigüedad cuidador", historial.cuidador_antiguedad),
        ("Contacto cuidador", f"{v(historial.cuidador_nombre)} / {v(historial.cuidador_telefono)}"),
        ("Decide asuntos familiares", sn(historial.decide_asuntos_familiares)),
        ("Relación familia", historial.relacion_familia),
        ("Problemas familiares", f"{sn(historial.problemas_familiares)} | {v(historial.tipo_problemas_familiares)}"),
        ("Medio transporte habitual", historial.medio_transporte_habitual),
        ("Pasa el día con", historial.pasa_dia_con),
    ], styles))
    story += bloque_texto("Costumbres y tradiciones", historial.costumbres_tradiciones, styles)
    story += bloque_texto("Actividades que le gusta realizar", historial.actividades_gusta, styles)
    story += bloque_texto("Actividades anteriores", historial.actividades_anteriores, styles)
    story += bloque_texto("Actividades actuales", historial.actividades_actuales, styles)
    story += bloque_texto("Riesgos en su entorno social", historial.riesgos_entorno_social, styles)

    story += titulo_seccion("ÁREA ESPIRITUAL", styles)
    story += bloque_texto("Sentido de vida", historial.sentido_vida, styles)
    story += bloque_texto("Misión de su vida", historial.mision_vida, styles)
    story.append(tabla_kv([
        ("Miedo a morir", sn(historial.miedo_morir)),
        ("Metas de vida", historial.metas_vida),
    ], styles))
    story += bloque_texto("Qué piensa sobre la muerte", historial.piensa_muerte, styles)
    story += bloque_texto("Principales miedos", historial.principales_miedos, styles)

    story += titulo_seccion("ÁREA PSICOLÓGICA", styles)
    story += bloque_texto("Episodios positivos", historial.episodios_positivos, styles)
    story.append(tabla_kv([
        ("Estado de ánimo", historial.estado_animo),
        ("Otro", historial.estado_animo_otro),
        ("Pérdidas", f"{sn(historial.perdidas)} | {v(historial.perdidas_cuales)}"),
        ("Duelo", f"{sn(historial.duelo)} | Tiempo: {v(historial.duelo_tiempo)} | Tipo: {v(historial.tipo_duelo)}"),
        ("Estrés", sn(historial.estres)),
        ("Ejercita memoria", f"{sn(historial.ejercita_memoria)} | {v(historial.ejercita_memoria_como)}"),
        ("Olvidos frecuentes", f"{sn(historial.olvidos_frecuentes)} | {v(historial.olvidos_cuales)}"),
        ("Satisfecho en su vida", f"{sn(historial.satisfecho_vida)} | {v(historial.satisfecho_vida_por_que)}"),
        ("Influye opinión demás", f"{sn(historial.influye_opinion_demas)} | {v(historial.influye_opinion_por_que)}"),
        ("Orientación", f"Persona: {v(historial.orientacion_persona)} | Espacio: {v(historial.orientacion_espacio)} | Tiempo: {v(historial.orientacion_tiempo)}"),
    ], styles))
    story += bloque_texto("Cómo afronta el estrés", historial.afronta_estres, styles)
    story += bloque_texto("Episodios negativos", historial.episodios_negativos, styles)
    story += bloque_texto("Comunicación verbal", historial.comunicacion_verbal, styles)
    story += bloque_texto("Comunicación no verbal", historial.comunicacion_no_verbal, styles)

    story += titulo_seccion("ÁREA FÍSICA", styles)
    story.append(tabla_kv([
        ("Incontinencia", sn(historial.incontinencia)),
        ("Urinaria / Fecal / Pañal", f"Urinaria: {sn(historial.incontinencia_urinaria)} | Fecal: {sn(historial.incontinencia_fecal)} | Pañal: {sn(historial.panal)}"),
        ("Estado general", historial.estado_general),
        ("Biotipo", historial.biotipo),
        ("Miembros superiores", sn(historial.miembros_superiores)),
        ("Miembros inferiores", sn(historial.miembros_inferiores)),
        ("Edema", sn(historial.edema)),
        ("Deformidades", f"{sn(historial.deformidades)} | {v(historial.deformidades_localizacion)}"),
        ("Úlceras vasculares", f"{sn(historial.ulceras_vasculares)} | {v(historial.ulceras_vasculares_localizacion)}"),
        ("Úlceras por presión", f"{sn(historial.ulceras_presion)} | {v(historial.ulceras_presion_localizacion)}"),
        ("Talla", historial.talla),
        ("Peso", historial.peso),
        ("Inmunizaciones", f"{sn(historial.inmunizaciones)} | {v(historial.inmunizaciones_cuales)}"),
        ("Miembros amputados", f"{sn(historial.miembros_amputados)} | {v(historial.miembros_amputados_cuales)}"),
        ("Horas durmiendo", historial.horas_durmiendo),
        ("Insomnio", sn(historial.insomnio)),
        ("Cirugías", f"{sn(historial.cirugias)} | {v(historial.cirugias_nombre)} | Año: {v(historial.cirugias_anio)}"),
        ("Antecedentes", f"{sn(historial.antecedentes)} | {v(historial.antecedentes_de_que)}"),
        ("Acepta", sn(historial.acepta)),
        ("Tipo de sangre", historial.tipo_sangre),
        ("Transfusiones", f"{sn(historial.transfusiones)} | {v(historial.transfusiones_cuales)}"),
        ("Alergias", f"{sn(historial.alergias)} | {v(historial.alergias_cuales)}"),
        ("FC Max", historial.fc_max),
        ("Temperatura corporal", historial.temperatura_corporal),
        ("Frecuencia cardiaca", historial.frecuencia_cardiaca),
        ("Frecuencia respiratoria", historial.frecuencia_respiratoria),
        ("Glucemia capilar", historial.glucemia_capilar),
        ("Tensión arterial", historial.tension_arterial),
        ("Actividad física", sn(historial.actividad_fisica)),
    ], styles))

    if pares:
        story += titulo_seccion("PARES CRANEALES / SALUD ORAL", styles)
        story.append(tabla_kv([
            ("Pares craneales evaluados", sn(pares.evaluados)),
            ("Sin alteraciones", sn(pares.sin_alteraciones)),
            ("Alteraciones", pares.alteraciones),
            ("Observaciones", pares.observaciones_generales),
            ("Dentadura postiza", sn(pares.dentadura_postiza)),
            ("Removible", sn(pares.removible)),
            ("Piezas perdidas", pares.piezas_perdidas),
            ("Piezas conservadas", pares.piezas_conservadas),
            ("Piezas frágiles", pares.piezas_fragiles),
            ("Problemas al masticar", sn(pares.problemas_masticar)),
            ("Consistencia alimentos", pares.consistencia_alimentos),
            ("Atragantamientos", sn(pares.atragantamientos)),
        ], styles))

    if marcha:
        story += titulo_seccion("MARCHA Y EQUILIBRIO", styles)
        story.append(tabla_kv([
            ("Cifosis", sn(marcha.cifosis)),
            ("Lordosis", sn(marcha.lordosis)),
            ("Escoliosis", sn(marcha.escoliosis)),
            ("Mareos", sn(marcha.mareos)),
            ("Síncope", sn(marcha.sincope)),
            ("Caídas", f"{sn(marcha.caidas)} | Frecuencia: {v(marcha.frecuencia_caidas)}"),
            ("Fracturas", f"{sn(marcha.fracturas)} | Antigüedad: {v(marcha.antiguedad_fracturas)}"),
            ("Consecuencias/secuelas", marcha.consecuencias_secuelas),
            ("Ayudas técnicas", marcha.ayudas_tecnicas),
        ], styles))

    if aphf:
        story += titulo_seccion("A.P.H.F. - ANTECEDENTES PATOLÓGICOS HEREDOFAMILIARES", styles)
        story.append(tabla_kv([
            ("Padre vive", sn(aphf.vive_padre)),
            ("Edad padre", aphf.edad_padre),
            ("Padecimientos padre", aphf.padecimientos_padre),
            ("Madre vive", sn(aphf.vive_madre)),
            ("Edad madre", aphf.edad_madre),
            ("Padecimientos madre", aphf.padecimientos_madre),
            ("Hermanos", aphf.numero_hermanos),
            ("Padecimientos hermanos", aphf.padecimientos_hermanos),
            ("Hijos", aphf.numero_hijos),
            ("Padecimientos hijos", aphf.padecimientos_hijos),
            ("Diabetes", sn(aphf.diabetes)),
            ("Hipertensión", sn(aphf.hipertension)),
            ("Cáncer", sn(aphf.cancer)),
            ("Cardiopatías", sn(aphf.cardiopatias)),
            ("Obesidad", sn(aphf.obesidad)),
            ("Demencia", sn(aphf.demencia)),
            ("Alzheimer", sn(aphf.alzheimer)),
            ("Parkinson", sn(aphf.parkinson)),
            ("Enfermedad renal", sn(aphf.enfermedad_renal)),
            ("Otra enfermedad", aphf.otra_enfermedad),
        ], styles))
        story += bloque_texto("Notas clínicas heredofamiliares", aphf.observaciones, styles)

    story += titulo_seccion("A.P.P. - ANTECEDENTES PATOLÓGICOS PERSONALES", styles)
    story.append(tabla_lista(
        ["Patología", "Hace cuánto", "Diagnóstico", "Fármaco", "Dosis"],
        [
            [x.patologia, x.hace_cuanto, x.diagnostico, x.farmaco, x.dosis]
            for x in app_patologias
        ],
        styles
    ))

    if app_resumen:
        story.append(Spacer(1, 6))
        story.append(tabla_kv([
            ("Número de embarazos", app_resumen.numero_embarazos),
            ("Fármacos no especificados", app_resumen.farmacos_no_especificados),
            ("Medicina alterna", app_resumen.medicina_alterna),
            ("", ""),
        ], styles))

    if factores:
        story += titulo_seccion("FACTORES DE RIESGO", styles)
        story.append(tabla_kv([
            ("Alcohol", f"{sn(factores.alcohol)} | Frecuencia: {v(factores.frecuencia_alcohol)}"),
            ("Tabaco", f"{sn(factores.tabaco)} | Frecuencia: {v(factores.frecuencia_tabaco)}"),
            ("Drogas", f"{sn(factores.drogas)} | Frecuencia: {v(factores.frecuencia_drogas)}"),
            ("Vida sexual activa", f"{sn(factores.vida_sexual_activa)} | Frecuencia: {v(factores.frecuencia_vida_sexual)}"),
            ("Observaciones", factores.observaciones),
            ("", ""),
        ], styles))

    story += titulo_seccion("ESTUDIOS COMPLEMENTARIOS (3 A 6 MESES)", styles)
    story.append(tabla_lista(
        ["Estudio", "Fecha", "Resultado", "Tratamiento"],
        [
            [x.estudio, x.fecha_estudio, x.resultado, x.tratamiento]
            for x in estudios
        ],
        styles
    ))

    story += titulo_seccion("VISITA AL MÉDICO / ESPECIALISTA", styles)
    story.append(tabla_lista(
        ["Fecha", "Especialista", "Motivo", "Tratamiento", "Estudios requeridos"],
        [
            [x.fecha_visita, x.especialista, x.motivo, x.tratamiento, x.estudios_requeridos]
            for x in visitas
        ],
        styles
    ))

    story.append(Spacer(1, 25))
    story.append(tabla_kv([
        ("Firma del responsable", "________________________________"),
        ("Firma del participante", "________________________________"),
    ], styles))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)

    buffer.seek(0)
    return buffer.getvalue()


@historial_clinico_bp.route("/<int:historial_id>/pdf")
@login_required
def historial_clinico_pdf(paciente_id, historial_id):
    paciente, historial = obtener_historial_por_id(paciente_id, historial_id)

    pdf_bytes = generar_pdf_historial_bytes(paciente, historial)
    buffer = BytesIO(pdf_bytes)

    nombre_archivo = f"historial_clinico_{paciente.id}_{historial.id}.pdf"

    return send_file(
        buffer,
        as_attachment=True,
        download_name=nombre_archivo,
        mimetype="application/pdf"
    )