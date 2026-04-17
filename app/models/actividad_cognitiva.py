from datetime import datetime
from app import db


class ActividadCognitiva(db.Model):
    __tablename__ = "actividad_cognitiva"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    actividad = db.Column(db.String(150), nullable=False)
    resultado = db.Column(db.String(300))
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_cognitivas")
    usuario = db.relationship("Usuario")