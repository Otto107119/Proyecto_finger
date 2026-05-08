from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from app.routes.actividad_cognitiva.utils import obtener_punto_corte, generar_resumen_clinico

def generar_pdf_actividad_cognitiva_bytes(consulta):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloReporte",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#1F4E3D"),
        spaceAfter=12
    )

    subtitulo_style = ParagraphStyle(
        "Subtitulo",
        parent=styles["Normal"],
        fontSize=10,
        alignment=1,
        textColor=colors.gray,
        spaceAfter=18
    )

    seccion_style = ParagraphStyle(
        "Seccion",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        textColor=colors.white,
        backColor=colors.HexColor("#198754"),
        spaceBefore=12,
        spaceAfter=8,
        leftIndent=4
    )

    texto_style = ParagraphStyle(
        "Texto",
        parent=styles["Normal"],
        fontSize=9,
        leading=12
    )

    story = []

    fecha = consulta.fecha_evaluacion or consulta.creado_en
    estado = "Finalizado" if consulta.finalizado else "En proceso"

    story.append(Paragraph("CAVIC Cognición del Adulto Mayor - Vigilancia CUValles", titulo_style))
    story.append(Paragraph("Reporte de Actividad Cognitiva", subtitulo_style))

    datos_generales = [
        ["Paciente", consulta.paciente.nombre or "-"],
        ["Fecha", fecha.strftime("%d/%m/%Y %H:%M") if fecha else "-"],
        ["Examinador", consulta.examinador or "-"],
        ["Edad", consulta.edad if consulta.edad is not None else "-"],
        ["Escolaridad", consulta.escolaridad_anios if consulta.escolaridad_anios is not None else "-"],
        ["Ocupación", consulta.ocupacion or "-"],
        ["Preferencia manual", consulta.preferencia_manual or "-"],
        ["Estado", estado],
    ]

    tabla_datos = Table(datos_generales, colWidths=[5 * cm, 10 * cm])
    tabla_datos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E9F5EF")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1F4E3D")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    story.append(Paragraph("Datos generales", seccion_style))
    story.append(tabla_datos)
    story.append(Spacer(1, 10))

    def valor(v):
        return v if v not in [None, ""] else "-"

    def agregar_tabla(titulo, filas):
        story.append(Paragraph(titulo, seccion_style))

        data = [["Campo", "Resultado", "Punto de corte"]]

        for fila in filas:
            if len(fila) == 2:
                data.append([fila[0], valor(fila[1]), "-"])
            else:
                data.append([fila[0], valor(fila[1]), fila[2]])

        tabla = Table(data, colWidths=[6.5 * cm, 4.5 * cm, 6 * cm])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D1E7DD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F5132")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ]))

        story.append(tabla)
        story.append(Spacer(1, 8))

    agregar_tabla("MOCA", [
        ["MOCA total", consulta.moca_total, obtener_punto_corte("moca")],
        ["Estimación MOCA", consulta.moca_estimacion],
    ])

    agregar_tabla("Dígitos", [
        ["Dígitos directos total", consulta.digitos_directos_total],
        ["Dígitos directos longitud", consulta.digitos_directos_longitud],
        ["Dígitos inversos total", consulta.digitos_inversos_total],
        ["Dígitos inversos longitud", consulta.digitos_inversos_longitud],
    ])

    agregar_tabla("Trail Making Test", [
        ["Trail A tiempo", f"{valor(consulta.trail_a_tiempo)} seg", obtener_punto_corte("trail_a")],
        ["Trail A errores", consulta.trail_a_errores],
        ["Trail A líneas correctas", consulta.trail_a_lineas_correctas],
        ["Trail A estimación", consulta.trail_a_estimacion],
        ["Trail B tiempo", f"{valor(consulta.trail_b_tiempo)} seg", obtener_punto_corte("trail_b")],
        ["Trail B errores", consulta.trail_b_errores],
        ["Trail B líneas correctas", consulta.trail_b_lineas_correctas],
        ["Trail B estimación", consulta.trail_b_estimacion],
        ["Puntuación diferencial", consulta.trail_puntuacion_diferencial],
        ["Puntuación ratio", consulta.trail_puntuacion_ratio],
    ])

    agregar_tabla("Lenguaje y fluidez", [
        ["MINT 32 total", consulta.mint_32_total, obtener_punto_corte("mint")],
        ["MINT 32 estimación", consulta.mint_32_estimacion],
        ["Fluencia P", consulta.fluencia_p],
        ["Fluencia M", consulta.fluencia_m],
        ["Promedio P/M", consulta.fluencia_pm_promedio, obtener_punto_corte("fluencia_pm")],
        ["Fluencia estimación", consulta.fluencia_estimacion],
        ["Animales total", consulta.animales_total, obtener_punto_corte("animales")],
        ["Vegetales total", consulta.vegetales_total, obtener_punto_corte("vegetales")],
        ["Fluidez semántica estimación", consulta.fluidez_semantica_estimacion],
    ])

    agregar_tabla("Memoria visual - Benson", [
        ["Benson inmediata", consulta.benson_inmediata],
        ["Benson diferida", consulta.benson_diferida],
        ["Porcentaje retenido", consulta.benson_porcentaje_retenido],
    ])

    agregar_tabla("Memoria verbal - Craft", [
        ["Craft RI 44", consulta.craft_ri_44],
        ["Craft RI paráfrase 25", consulta.craft_ri_parafraseo_25],
        ["Craft RD 44", consulta.craft_rd_44],
        ["Craft RD paráfrase 25", consulta.craft_rd_parafraseo_25],
        ["Porcentaje retenido Craft", consulta.craft_porcentaje_retenido],
        ["Diferencia retención verbal/visual", consulta.diferencia_retencion_verbal_visual],
    ])

    agregar_tabla("Resultado global", [
        ["Estimación global", consulta.estimacion_global],
    ])

    resumen_clinico = generar_resumen_clinico(consulta)

    story.append(Paragraph("Resumen clínico automático", seccion_style))
    story.append(Paragraph(resumen_clinico, texto_style))

    doc.build(story)

    buffer.seek(0)
    return buffer
