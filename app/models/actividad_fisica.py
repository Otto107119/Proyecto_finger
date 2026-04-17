from datetime import datetime
from app import db


class ActividadFisica(db.Model):
    __tablename__ = "actividad_fisica"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    duracion_min = db.Column(db.Integer, nullable=False)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_fisicas")
    usuario = db.relationship("Usuario")