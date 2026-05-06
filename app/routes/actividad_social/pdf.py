from io import BytesIO

from flask import render_template, make_response
from flask_login import login_required
from xhtml2pdf import pisa

from app.models import ActividadSocial, Paciente
from . import actividad_social_bp


def generar_pdf_actividad_social_bytes(paciente, actividad):
    html = render_template(
        "actividad_social/pdf_actividad_social.html",
        actividad=actividad,
        paciente=paciente
    )

    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        return None

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


@actividad_social_bp.route("/<int:actividad_id>/pdf")
@login_required
def actividad_social_pdf(paciente_id, actividad_id):
    actividad = ActividadSocial.query.filter_by(
        id=actividad_id,
        paciente_id=paciente_id
    ).first_or_404()

    paciente = Paciente.query.get_or_404(paciente_id)

    pdf = generar_pdf_actividad_social_bytes(paciente, actividad)

    if pdf is None:
        return "Error al generar el PDF", 500

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f"inline; filename=actividad_social_{actividad.id}_paciente_{paciente.id}.pdf"
    )

    return response