from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generar_pdf_area_medica_bytes(paciente, registro):
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
        "TituloAreaMedica",
        parent=styles["Title"],
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#842029"),
        spaceAfter=8
    )

    subtitulo_style = ParagraphStyle(
        "SubtituloAreaMedica",
        parent=styles["Normal"],
        fontSize=10,
        alignment=1,
        textColor=colors.gray,
        spaceAfter=18
    )

    seccion_style = ParagraphStyle(
        "SeccionAreaMedica",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        textColor=colors.white,
        backColor=colors.HexColor("#DC3545"),
        spaceBefore=12,
        spaceAfter=8,
        leftIndent=4
    )

    story = []

    def valor(v):
        return v if v not in [None, ""] else "-"

    def si_no(v):
        return "Sí" if v else "No"

    def tabla_resultados(titulo, filas):
        story.append(Paragraph(titulo, seccion_style))

        data = [["Campo", "Resultado"]]

        for campo, resultado in filas:
            data.append([campo, valor(resultado)])

        tabla = Table(data, colWidths=[7 * cm, 8 * cm])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F8D7DA")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#842029")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 1), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.white,
                colors.HexColor("#F8F9FA")
            ]),
        ]))

        story.append(tabla)
        story.append(Spacer(1, 8))

    story.append(Paragraph("CAVIC Cognición del Adulto Mayor - Vigilancia CUValles", titulo_style))
    story.append(Paragraph("Reporte de Área Médica", subtitulo_style))

    fecha = (
        registro.fecha_registro.strftime("%d/%m/%Y %H:%M")
        if registro.fecha_registro else "-"
    )

    tabla_resultados("Datos del paciente", [
        ["Paciente", paciente.nombre],
        ["Fecha de registro", fecha],
        ["Edad", registro.edad],
        ["Sexo", registro.sexo],
    ])

    tabla_resultados("Riesgo cardiovascular", [
        ["Presión sistólica", f"{valor(registro.presion_sistolica)} mmHg"],
        ["Tratamiento por hipertensión", si_no(registro.tratamiento_hipertension)],
        ["Fumador", si_no(registro.fumador)],
        ["Diabético", si_no(registro.diabetico)],
        ["HDL", valor(registro.hdl)],
        ["Colesterol", valor(registro.colesterol)],
        ["Edad del corazón", valor(registro.edad_corazon)],
        ["Porcentaje de riesgo", f"{valor(registro.porcentaje_riesgo)}%"],
        ["Interpretación", registro.interpretacion_riesgo or "No calculado"],
    ])

    tabla_resultados("Laboratoriales", [
        ["Colesterol total", f"{valor(registro.colesterol_total)} mg/dL"],
        ["Colesterol LDL", f"{valor(registro.colesterol_ldl)} mg/dL"],
        ["Colesterol HDL", f"{valor(registro.colesterol_hdl)} mg/dL"],
        ["Triglicéridos", f"{valor(registro.trigliceridos)} mg/dL"],
        ["Glucosa capilar", f"{valor(registro.glucosa_capilar)} mg/dL"],
    ])

    tabla_resultados("Valores de referencia", [
        ["Colesterol total", "< 200 mg/dL"],
        ["Colesterol LDL", "< 100 mg/dL"],
        ["Colesterol HDL", "40 - 60 mg/dL"],
        ["Triglicéridos", "< 150 mg/dL"],
        ["Glucosa capilar", "70 - 110 mg/dL"],
    ])

    doc.build(story)
    buffer.seek(0)

    return buffer