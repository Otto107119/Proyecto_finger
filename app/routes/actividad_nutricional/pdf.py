from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def generar_pdf_actividad_nutricional_bytes(actividad):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        "TituloReporteNutricional",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#1F4E3D"),
        spaceAfter=8
    )

    subtitulo_style = ParagraphStyle(
        "SubtituloNutricional",
        parent=styles["Normal"],
        fontSize=10,
        alignment=1,
        textColor=colors.gray,
        spaceAfter=18
    )

    seccion_style = ParagraphStyle(
        "SeccionNutricional",
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
        "TextoNutricional",
        parent=styles["Normal"],
        fontSize=9,
        leading=12
    )

    story = []

    def valor(v):
        return v if v not in [None, ""] else "-"

    def si_no(v):
        return "Sí" if v else "No"

    def tabla_simple(filas, col1=6 * cm, col2=9 * cm):
        tabla = Table(filas, colWidths=[col1, col2])
        tabla.setStyle(TableStyle([
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
        return tabla

    def tabla_resultados(titulo, filas):
        story.append(Paragraph(titulo, seccion_style))

        data = [["Campo", "Resultado"]]
        for campo, resultado in filas:
            data.append([campo, valor(resultado)])

        tabla = Table(data, colWidths=[7 * cm, 8 * cm])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D1E7DD")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F5132")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
        ]))

        story.append(tabla)
        story.append(Spacer(1, 8))

    story.append(Paragraph("CAVIC Cognición del Adulto Mayor - Vigilancia CUValles", titulo_style))
    story.append(Paragraph("Reporte de Actividad Nutricional", subtitulo_style))

    fecha = actividad.fecha_registro.strftime("%d/%m/%Y %H:%M") if actividad.fecha_registro else "-"

    story.append(Paragraph("Datos del paciente", seccion_style))
    story.append(tabla_simple([
        ["Paciente", actividad.paciente.nombre],
        ["Fecha de registro", fecha],
    ]))
    story.append(Spacer(1, 8))

    tabla_resultados("Datos generales", [
        ["Problemas de masticación/deglución", si_no(actividad.problemas_masticacion_deglucion)],
        ["Alergias a alimentos", si_no(actividad.alergias_alimentos)],
        ["Intolerancias a alimentos", si_no(actividad.intolerancias_alimentos)],
        ["Peso", f"{actividad.peso} kg" if actividad.peso is not None else "-"],
        ["Talla", f"{actividad.talla} cm" if actividad.talla is not None else "-"],
        ["IMC", actividad.imc],
        ["Cintura", f"{actividad.cintura} cm" if actividad.cintura is not None else "-"],
        ["Cadera", f"{actividad.cadera} cm" if actividad.cadera is not None else "-"],
        ["Pantorrilla", f"{actividad.pantorrilla} cm" if actividad.pantorrilla is not None else "-"],
    ])

    tabla_resultados("Índice de calidad de la dieta", [
        ["Consume frutas diariamente", si_no(actividad.frutas_diarias)],
        ["Consume verduras diariamente", si_no(actividad.verduras_diarias)],
        ["Leguminosas >= 3 veces por semana", si_no(actividad.leguminosas)],
        ["Proteína adecuada diariamente", si_no(actividad.proteina_adecuada)],
        ["Prefiere cereales integrales", si_no(actividad.cereales_integrales)],
        ["Limita refrescos y jugos", si_no(actividad.limita_refrescos_jugos)],
        ["Limita embutidos/procesados", si_no(actividad.limita_embutidos_procesados)],
        ["Agua >= 1.5 L/día", si_no(actividad.agua_suficiente)],
        ["Incluye grasas saludables", si_no(actividad.grasas_saludables)],
        ["Más de 3 tiempos de comida", si_no(actividad.mas_de_tres_comidas)],
        ["Puntaje", f"{actividad.puntaje_calidad_dieta}/10"],
        ["Interpretación", actividad.interpretacion_calidad_dieta],
    ])

    tabla_resultados("Mini Nutritional Assessment - MNA-SF", [
        ["Ingesta", actividad.mna_ingesta],
        ["Pérdida de peso", actividad.mna_perdida_peso],
        ["Movilidad", actividad.mna_movilidad],
        ["Estrés/enfermedad aguda", actividad.mna_estres],
        ["Problemas neuropsicológicos", actividad.mna_neuropsicologicos],
        ["IMC/Pantorrilla", actividad.mna_imc],
        ["Puntaje", f"{actividad.puntaje_mna}/14"],
        ["Interpretación", actividad.interpretacion_mna],
    ])

    story.append(Paragraph("Recordatorio de 24 horas", seccion_style))

    recordatorio_data = [[
        "Tiempo", "Frutas", "Verduras", "Cereales", "Lácteos",
        "Legum.", "AOA", "Aceites", "Café", "Azúcar", "Frutos secos"
    ]]

    for r in actividad.recordatorios:
        recordatorio_data.append([
            valor(r.tiempo_comida),
            valor(r.frutas),
            valor(r.verduras),
            valor(r.cereales),
            valor(r.lacteos),
            valor(r.leguminosas),
            valor(r.aoa),
            valor(r.aceites_grasas),
            valor(r.cafe),
            valor(r.azucar),
            valor(r.frutos_secos),
        ])

    tabla_recordatorio = Table(
        recordatorio_data,
        colWidths=[
            2.3 * cm, 1.25 * cm, 1.35 * cm, 1.35 * cm, 1.25 * cm,
            1.25 * cm, 1.1 * cm, 1.25 * cm, 1.1 * cm, 1.1 * cm, 1.55 * cm
        ],
        repeatRows=1
    )

    tabla_recordatorio.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D1E7DD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F5132")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))

    story.append(tabla_recordatorio)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Frecuencia de grasas", seccion_style))

    grasas_data = [["Tipo de grasa", "Utiliza", "Frecuencia"]]

    for g in actividad.frecuencia_grasas:
        grasas_data.append([
            valor(g.tipo_grasa),
            si_no(g.utiliza),
            valor(g.frecuencia),
        ])

    tabla_grasas = Table(grasas_data, colWidths=[8 * cm, 3 * cm, 4 * cm], repeatRows=1)
    tabla_grasas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D1E7DD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F5132")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
    ]))

    story.append(tabla_grasas)

    doc.build(story)
    buffer.seek(0)
    
    return buffer