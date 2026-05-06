from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def valor(valor, unidad=""):
    if valor is None or valor == "":
        return "-"

    if unidad:
        return f"{valor} {unidad}"

    return str(valor)


def obtener_nombre_paciente(paciente):
    partes = []

    for campo in ["nombre", "apellido_paterno", "apellido_materno"]:
        dato = getattr(paciente, campo, None)
        if dato:
            partes.append(str(dato))

    return " ".join(partes) if partes else "Paciente sin nombre"


def crear_tabla(datos, color_encabezado):
    tabla = Table(datos, colWidths=[260, 220])

    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(color_encabezado)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#b0b0b0")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8f9fa")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    return tabla


def generar_pdf_actividad_fisica_bytes(paciente, evaluacion):
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

    styles.add(ParagraphStyle(
        name="TituloCentrado",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        spaceAfter=14
    ))

    styles.add(ParagraphStyle(
        name="Subtitulo",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#343a40"),
        spaceBefore=10,
        spaceAfter=8
    ))

    elementos = []

    nombre_paciente = obtener_nombre_paciente(paciente)

    fecha = evaluacion.fecha.strftime("%d/%m/%Y") if evaluacion.fecha else "-"

    elementos.append(Paragraph("Evaluación de Actividad Física", styles["TituloCentrado"]))
    elementos.append(Spacer(1, 8))

    datos_paciente = [
        ["Paciente", nombre_paciente],
        ["Fecha de evaluación", fecha],
    ]

    elementos.append(crear_tabla(datos_paciente, "#343a40"))
    elementos.append(Spacer(1, 18))

    datos_generales = [
        ["Prueba", "Resultado"],
        ["Sentarse y levantarse 30 s", valor(evaluacion.sentarse_levantarse_30s, "repeticiones")],
        ["Dinamómetro", valor(evaluacion.dinamometro_kg, "kg")],
        ["TUG", valor(evaluacion.tug_segundos, "segundos")],
        ["Equilibrio unipodal", valor(evaluacion.equilibrio_unipodal_segundos, "segundos")],
        ["Caminata 6 minutos", valor(evaluacion.caminata_6min_metros, "metros")],
        ["Velocidad de marcha", valor(evaluacion.velocidad_marcha_ms, "m/s")],
    ]

    elementos.append(Paragraph("Evaluaciones físicas generales", styles["Subtitulo"]))
    elementos.append(crear_tabla(datos_generales, "#0d6efd"))
    elementos.append(Spacer(1, 18))

    datos_sppb = [
        ["Dimensión", "Puntaje"],
        ["Equilibrio", f"{evaluacion.sppb_equilibrio or 0}/4"],
        ["Velocidad de marcha", f"{evaluacion.sppb_velocidad_marcha or 0}/4"],
        ["Fuerza de piernas", f"{evaluacion.sppb_fuerza_piernas or 0}/4"],
        ["Total SPPB", f"{evaluacion.sppb_total or 0}/12"],
        ["Interpretación", evaluacion.interpretacion_sppb or "-"],
    ]

    elementos.append(Paragraph("Resultado SPPB", styles["Subtitulo"]))
    elementos.append(crear_tabla(datos_sppb, "#198754"))
    elementos.append(Spacer(1, 18))

    datos_interpretacion = [
        ["Indicador", "Resultado"],
        ["Riesgo de caída", evaluacion.riesgo_caida or "-"],
        ["Riesgo funcional", evaluacion.riesgo_funcional or "-"],
    ]

    elementos.append(Paragraph("Interpretación funcional", styles["Subtitulo"]))
    elementos.append(crear_tabla(datos_interpretacion, "#6c757d"))
    elementos.append(Spacer(1, 18))

    if evaluacion.notas:
        elementos.append(Paragraph("Notas clínicas", styles["Subtitulo"]))
        elementos.append(Paragraph(str(evaluacion.notas), styles["Normal"]))

    doc.build(elementos)

    buffer.seek(0)
    return buffer