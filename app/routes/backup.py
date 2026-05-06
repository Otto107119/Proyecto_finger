import os
import zipfile
from io import BytesIO
from datetime import datetime

from flask import Blueprint, send_file, abort
from flask_login import login_required, current_user

from app import db

from app.models.actividad_fisica import ActividadFisica
from app.models.actividad_cognitiva import ActividadCognitiva
from app.models.actividad_nutricional import ActividadNutricional
from app.models.area_medica import AreaMedica
from app.models import Paciente, HistorialClinico, ActividadSocial

from app.routes.actividad_fisica.pdf import generar_pdf_actividad_fisica_bytes
from app.routes.actividad_cognitiva.pdf import generar_pdf_actividad_cognitiva_bytes
from app.routes.actividad_nutricional.pdf import generar_pdf_actividad_nutricional_bytes
from app.routes.area_medica.pdf import generar_pdf_area_medica_bytes
from app.routes.actividad_social.pdf import generar_pdf_actividad_social_bytes
from app.routes.historial_clinico.pdf import generar_pdf_historial_bytes


backup_bp = Blueprint("backup", __name__, url_prefix="/backup")


@backup_bp.route("/completo")
@login_required
def respaldo_completo():
    if current_user.rol not in ["superadmin", "superadministrador"]:
        abort(403)

    memoria_zip = BytesIO()
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_zip = f"respaldo_completo_{fecha}.zip"

    with zipfile.ZipFile(memoria_zip, "w", zipfile.ZIP_DEFLATED) as zipf:

        # Base de datos
        db_path = db.engine.url.database

        if db_path:
            db_path = os.path.abspath(db_path)

            if os.path.exists(db_path):
                zipf.write(
                    db_path,
                    arcname=f"base_datos/{os.path.basename(db_path)}"
                )


        # PDFs de actividad física
        evaluaciones_fisicas = ActividadFisica.query.all()

        for evaluacion in evaluaciones_fisicas:
            paciente = Paciente.query.get(evaluacion.paciente_id)

            if not paciente:
                continue

            pdf_buffer = generar_pdf_actividad_fisica_bytes(paciente, evaluacion)

            if not pdf_buffer:
                continue

            nombre_pdf = f"actividad_fisica_{evaluacion.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"actividad_fisica_pdf/{nombre_pdf}",
                pdf_buffer.getvalue()
            )

                    # PDFs de actividad cognitiva
        actividades_cognitivas = ActividadCognitiva.query.all()

        if not actividades_cognitivas:
            zipf.writestr(
                "actividad_cognitiva_pdf/sin_registros.txt",
                "No existen registros de actividad cognitiva."
            )

        for consulta in actividades_cognitivas:
            paciente = consulta.paciente

            if not paciente:
                continue

            pdf_buffer = generar_pdf_actividad_cognitiva_bytes(consulta)

            if not pdf_buffer:
                continue

            nombre_pdf = f"actividad_cognitiva_{consulta.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"actividad_cognitiva_pdf/{nombre_pdf}",
                pdf_buffer.getvalue()
            )

        # PDFs de actividad nutricional
        actividades_nutricionales = ActividadNutricional.query.all()

        if not actividades_nutricionales:
            zipf.writestr(
                "actividad_nutricional_pdf/sin_registros.txt",
                "No existen registros de actividad nutricional."
            )

        for actividad in actividades_nutricionales:
            paciente = actividad.paciente

            if not paciente:
                continue

            pdf_buffer = generar_pdf_actividad_nutricional_bytes(actividad)

            if not pdf_buffer:
                continue

            nombre_pdf = f"actividad_nutricional_{actividad.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"actividad_nutricional_pdf/{nombre_pdf}",
                pdf_buffer.getvalue()
            )

                # PDFs de área médica
        registros_medicos = AreaMedica.query.all()

        if not registros_medicos:
            zipf.writestr(
                "area_medica_pdf/sin_registros.txt",
                "No existen registros de área médica."
            )

        for registro in registros_medicos:
            paciente = registro.paciente

            if not paciente:
                continue

            pdf_buffer = generar_pdf_area_medica_bytes(paciente, registro)

            if not pdf_buffer:
                continue

            nombre_pdf = f"area_medica_{registro.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"area_medica_pdf/{nombre_pdf}",
                pdf_buffer.getvalue()
            )
            
            # PDFs de actividad social
        actividades_sociales = ActividadSocial.query.all()

        for actividad in actividades_sociales:
            paciente = actividad.paciente

            if not paciente:
                continue

            pdf_bytes = generar_pdf_actividad_social_bytes(paciente, actividad)

            if not pdf_bytes:
                continue

            nombre_pdf = f"actividad_social_{actividad.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"actividad_social_pdf/{nombre_pdf}",
                pdf_bytes
            )
            
            # PDFs de historiales clínicos
        historiales = HistorialClinico.query.all()

        for historial in historiales:
            paciente = historial.paciente

            if not paciente:
                continue

            pdf_bytes = generar_pdf_historial_bytes(paciente, historial)

            if not pdf_bytes:
                continue

            nombre_pdf = f"historial_{historial.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"historiales_clinicos_pdf/{nombre_pdf}",
                pdf_bytes
            )

        # Información general
        pacientes_count = Paciente.query.count()
        actividad_fisica_count = ActividadFisica.query.count()
        actividad_cognitiva_count = ActividadCognitiva.query.count()
        actividad_nutricional_count = ActividadNutricional.query.count()
        area_medica_count = AreaMedica.query.count()
        actividad_social_count = ActividadSocial.query.count()
        historiales_count = HistorialClinico.query.count()

        info = f"""
RESPALDO COMPLETO DEL SISTEMA

Fecha de respaldo: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Generado por: {current_user.nombre}
Rol: {current_user.rol}

Pacientes registrados: {pacientes_count}
Evaluaciones de actividad física registradas: {actividad_fisica_count}
Registros de actividad cognitiva: {actividad_cognitiva_count}
Capturas de actividad nutricional registradas: {actividad_nutricional_count}
Registros de área médica: {area_medica_count}
Capturas de actividad social registradas: {actividad_social_count}
Historiales clínicos registrados: {historiales_count}

Contenido:
- Copia de base de datos
- PDFs de actividad física
- PDFs de actividad cognitiva
- PDFs de actividad nutricional
- PDFs de área médica
- PDFs de actividad social
- PDFs de historiales clínicos

Nota:
Este respaldo debe almacenarse en un lugar seguro.
"""

        zipf.writestr("info_respaldo.txt", info)

    memoria_zip.seek(0)

    return send_file(
        memoria_zip,
        as_attachment=True,
        download_name=nombre_zip,
        mimetype="application/zip"
    )