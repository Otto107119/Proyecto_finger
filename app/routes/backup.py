import os
import zipfile
from io import BytesIO
from datetime import datetime

from flask import Blueprint, send_file, abort
from flask_login import login_required, current_user

from app import db
from app.models import Paciente, HistorialClinico
from app.routes.historial_clinico.pdf import generar_pdf_historial_bytes

backup_bp = Blueprint("backup", __name__, url_prefix="/backup")


@backup_bp.route("/completo")
@login_required
def respaldo_completo():
    if current_user.rol != "superadmin":
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

        # PDFs de historiales clínicos
        historiales = HistorialClinico.query.all()

        for historial in historiales:
            paciente = historial.paciente

            if not paciente:
                continue

            pdf_bytes = generar_pdf_historial_bytes(paciente, historial)
            nombre_pdf = f"historial_{historial.id}_paciente_{paciente.id}.pdf"

            zipf.writestr(
                f"historiales_clinicos_pdf/{nombre_pdf}",
                pdf_bytes
            )

        # Información general
        pacientes_count = Paciente.query.count()
        historiales_count = HistorialClinico.query.count()

        info = f"""
RESPALDO COMPLETO DEL SISTEMA

Fecha de respaldo: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
Generado por: {current_user.nombre}
Rol: {current_user.rol}

Pacientes registrados: {pacientes_count}
Historiales clínicos registrados: {historiales_count}

Contenido:
- Copia de base de datos
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