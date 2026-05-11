from io import BytesIO

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def estimacion_por_percentil(percentil):
    if percentil is None:
        return "-"

    if percentil < 1:
        return "Severamente deteriorado"
    elif percentil < 2:
        return "Moderadamente deteriorado"
    elif percentil < 9:
        return "Levemente deteriorado"
    elif percentil < 25:
        return "Promedio bajo"
    elif percentil < 75:
        return "Promedio"
    elif percentil < 91:
        return "Promedio alto"
    elif percentil < 98:
        return "Superior"

    return "Muy superior"

def generar_pdf_actividad_cognitiva_bytes(consulta):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloReporte",
        parent=styles["Title"],
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#0D6EFD"),
        spaceAfter=8
    )

    subtitulo_style = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontSize=9,
        alignment=1,
        textColor=colors.gray,
        spaceAfter=12
    )

    seccion_style = ParagraphStyle(
        "Seccion",
        parent=styles["Heading2"],
        fontSize=10,
        leading=12,
        textColor=colors.white,
        backColor=colors.HexColor("#212529"),
        spaceBefore=10,
        spaceAfter=6,
        leftIndent=4
    )

    texto_style = ParagraphStyle(
        "Texto",
        parent=styles["Normal"],
        fontSize=8,
        leading=10
    )

    story = []

    def valor(v):
        return v if v not in [None, ""] else "-"

    def fmt(v):
        if v in [None, ""]:
            return "-"
        if isinstance(v, float):
            return round(v, 3)
        return v

    fecha = consulta.fecha_evaluacion
    estado = "Finalizado" if consulta.finalizado else "En proceso"

    story.append(Paragraph("CAVIC CUValles", titulo_style))
    story.append(Paragraph("Reporte de Actividad Cognitiva - UDS-3", subtitulo_style))

    # =========================
    # DATOS GENERALES
    # =========================
    datos_generales = [
        ["Paciente", valor(consulta.paciente.nombre)],
        ["Fecha", fecha.strftime("%d/%m/%Y") if fecha else "-"],
        ["Examinador", valor(consulta.examinador)],
        ["Edad", valor(consulta.edad)],
        ["Sexo", valor(consulta.sexo)],
        ["Escolaridad", valor(consulta.escolaridad_anios)],
        ["Idioma", valor(consulta.idioma)],
        ["Ocupación", valor(consulta.ocupacion)],
        ["Preferencia manual", valor(consulta.preferencia_manual)],
        ["Estado", estado],
    ]

    story.append(Paragraph("Datos generales", seccion_style))

    tabla_datos = Table(datos_generales, colWidths=[4 * cm, 9 * cm])
    tabla_datos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E9F2FF")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0D6EFD")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    story.append(tabla_datos)
    story.append(Spacer(1, 8))

    # =========================
    # ESTIMACIÓN GENERAL
    # =========================
    story.append(Paragraph("Estimación general", seccion_style))
    story.append(Paragraph(f"<b>{valor(consulta.estimacion_global)}</b>", texto_style))
    story.append(Paragraph(valor(consulta.perfil_cognitivo), texto_style))
    story.append(Spacer(1, 8))

    # =========================
    # RESULTADOS NORMATIVOS
    # =========================
    story.append(Paragraph("Resultados normativos UDS-3", seccion_style))

    resultados = [
        ["Proceso", "Prueba", "Puntaje bruto", "Z-score", "Percentil", "Estimación"],

        ["Screening", "MOCA", f"{valor(consulta.moca_total)}/30", fmt(consulta.moca_z), fmt(consulta.moca_percentil), valor(consulta.moca_estimacion)],

        ["Atención", "Dígitos directos total", f"{valor(consulta.digitos_directos_total)}/14", fmt(consulta.digitos_directos_total_z), fmt(consulta.digitos_directos_total_percentil), estimacion_por_percentil(consulta.digitos_directos_total_percentil)],
        ["Atención", "Dígitos directos longitud", f"{valor(consulta.digitos_directos_longitud)}/9", fmt(consulta.digitos_directos_longitud_z), fmt(consulta.digitos_directos_longitud_percentil), estimacion_por_percentil(consulta.digitos_directos_longitud_percentil)],
        ["Atención", "Dígitos inversos total", f"{valor(consulta.digitos_inversos_total)}/8", fmt(consulta.digitos_inversos_total_z), fmt(consulta.digitos_inversos_total_percentil), estimacion_por_percentil(consulta.digitos_inversos_total_percentil)],
        ["Atención", "Dígitos inversos longitud", f"{valor(consulta.digitos_inversos_longitud)}/8", fmt(consulta.digitos_inversos_longitud_z), fmt(consulta.digitos_inversos_longitud_percentil), estimacion_por_percentil(consulta.digitos_inversos_longitud_percentil)],

        ["Atención sostenida", "Trail Making Test A", f"{valor(consulta.trail_a_tiempo)} seg.", fmt(consulta.trail_a_z), fmt(consulta.trail_a_percentil), estimacion_por_percentil(consulta.trail_a_percentil)],
        ["Función ejecutiva", "Trail Making Test B", f"{valor(consulta.trail_b_tiempo)} seg.", fmt(consulta.trail_b_z), fmt(consulta.trail_b_percentil), estimacion_por_percentil(consulta.trail_b_percentil)],

        ["Búsqueda léxica", "MINT-32", f"{valor(consulta.mint_32_total)}/32", fmt(consulta.mint_32_z), fmt(consulta.mint_32_percentil), valor(consulta.mint_32_estimacion)],

        ["Fluencia fonológica", "Letra P", valor(consulta.fluencia_p), fmt(consulta.fluencia_p_z), fmt(consulta.fluencia_p_percentil), estimacion_por_percentil(consulta.fluencia_p_percentil)],
        ["Fluencia fonológica", "Letra M", valor(consulta.fluencia_m), fmt(consulta.fluencia_m_z), fmt(consulta.fluencia_m_percentil), estimacion_por_percentil(consulta.fluencia_m_percentil)],
        ["Fluencia fonológica", "Total P + M", valor(consulta.fluencia_pm_total), fmt(consulta.fluencia_pm_z), fmt(consulta.fluencia_pm_percentil), estimacion_por_percentil(consulta.fluencia_pm_percentil)],

        ["Fluidez semántica", "Animales", valor(consulta.fluidez_animales), fmt(consulta.fluidez_animales_z), fmt(consulta.fluidez_animales_percentil), estimacion_por_percentil(consulta.fluidez_animales_percentil)],
        ["Fluidez semántica", "Vegetales", valor(consulta.fluidez_vegetales), fmt(consulta.fluidez_vegetales_z), fmt(consulta.fluidez_vegetales_percentil), estimacion_por_percentil(consulta.fluidez_vegetales_percentil)],

        ["Memoria visual", "Benson copia", f"{valor(consulta.benson_copia_total)}/10", fmt(consulta.benson_copia_z), fmt(consulta.benson_copia_percentil), estimacion_por_percentil(consulta.benson_copia_percentil)],
        ["Memoria visual", "Benson recuerdo", f"{valor(consulta.benson_recuerdo_total)}/10", fmt(consulta.benson_recuerdo_z), fmt(consulta.benson_recuerdo_percentil), estimacion_por_percentil(consulta.benson_recuerdo_percentil)],
        ["Memoria visual", "Benson % retenido", f"{valor(consulta.benson_porcentaje_retenido)}%", fmt(consulta.benson_retencion_z), fmt(consulta.benson_retencion_percentil), estimacion_por_percentil(consulta.benson_retencion_percentil)],

        ["Memoria verbal", "Craft inmediato textual", f"{valor(consulta.craft_inmediato_textual)}/44", fmt(consulta.craft_inmediato_textual_z), fmt(consulta.craft_inmediato_textual_percentil), estimacion_por_percentil(consulta.craft_inmediato_textual_percentil)],
        ["Memoria verbal", "Craft inmediato parafraseo", f"{valor(consulta.craft_inmediato_parafraseo)}/25", fmt(consulta.craft_inmediato_parafraseo_z), fmt(consulta.craft_inmediato_parafraseo_percentil), estimacion_por_percentil(consulta.craft_inmediato_parafraseo_percentil)],
        ["Memoria verbal", "Craft diferido textual", f"{valor(consulta.craft_diferido_textual)}/44", fmt(consulta.craft_diferido_textual_z), fmt(consulta.craft_diferido_textual_percentil), estimacion_por_percentil(consulta.craft_diferido_textual_percentil)],
        ["Memoria verbal", "Craft diferido parafraseo", f"{valor(consulta.craft_diferido_parafraseo)}/25", fmt(consulta.craft_diferido_parafraseo_z), fmt(consulta.craft_diferido_parafraseo_percentil), estimacion_por_percentil(consulta.craft_diferido_parafraseo_percentil)],
        ["Memoria verbal", "Craft % retenido", f"{valor(consulta.craft_porcentaje_retenido)}%", fmt(consulta.craft_retencion_z), fmt(consulta.craft_retencion_percentil), estimacion_por_percentil(consulta.craft_retencion_percentil)],
    ]

    tabla_resultados = Table(
        resultados,
        colWidths=[3.3 * cm, 5.2 * cm, 3 * cm, 2.3 * cm, 2.4 * cm, 3.4 * cm],
        repeatRows=1
    )

    tabla_resultados.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#212529")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))

    story.append(tabla_resultados)
    story.append(Spacer(1, 8))

    # =========================
    # ÍNDICES DERIVADOS
    # =========================
    story.append(Paragraph("Índices derivados", seccion_style))

    indices = [
        ["Índice", "Valor", "Z-score", "Percentil"],
        ["Trail diferencial B-A", valor(consulta.trail_diferencial), fmt(consulta.trail_diferencial_z), fmt(consulta.trail_diferencial_percentil)],
        ["Trail ratio B/A", valor(consulta.trail_ratio), fmt(consulta.trail_ratio_z), fmt(consulta.trail_ratio_percentil)],
        ["Diferencial semántico/fonológico", valor(consulta.fluencia_semantica_fonologica_diferencial), fmt(consulta.fluencia_semantica_fonologica_z), fmt(consulta.fluencia_semantica_fonologica_percentil)],
        ["Índice de errores", valor(consulta.indice_errores), fmt(consulta.indice_errores_z), fmt(consulta.indice_errores_percentil)],
        ["Diferencia verbal/visual", valor(consulta.diferencia_retencion_verbal_visual), fmt(consulta.diferencia_retencion_verbal_visual_z), fmt(consulta.diferencia_retencion_verbal_visual_percentil)],
    ]

    tabla_indices = Table(indices, colWidths=[7 * cm, 4 * cm, 4 * cm, 4 * cm])
    tabla_indices.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#212529")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))

    story.append(tabla_indices)
    story.append(Spacer(1, 8))

    # =========================
    # SUEÑO
    # =========================
    story.append(Paragraph("Calidad del sueño", seccion_style))

    sueno = [
        ["Índice de calidad de sueño", valor(consulta.sueno_indice_calidad)],
        ["Estimación", valor(consulta.sueno_estimacion)],
        ["Observaciones", valor(consulta.sueno_observaciones)],
    ]

    tabla_sueno = Table(sueno, colWidths=[5 * cm, 14 * cm])
    tabla_sueno.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E9F2FF")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0D6EFD")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
    ]))

    story.append(tabla_sueno)

    doc.build(story)

    buffer.seek(0)
    return buffer
