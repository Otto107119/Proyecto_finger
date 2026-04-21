from app import db
from app.models import Paciente, HistorialClinico


def obtener_historial(paciente_id):
    paciente = Paciente.query.get_or_404(paciente_id)

    historial = HistorialClinico.query.filter_by(paciente_id=paciente.id).first()
    if not historial:
        historial = HistorialClinico(paciente_id=paciente.id)
        db.session.add(historial)
        db.session.commit()

    return paciente, historial