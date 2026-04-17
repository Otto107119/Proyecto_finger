from datetime import datetime
from app import db


class ActividadMedica(db.Model):
    __tablename__ = "actividad_medica"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    presion_arterial = db.Column(db.String(20))
    glucosa = db.Column(db.String(20))
    peso = db.Column(db.Float)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_medicas")
    usuario = db.relationship("Usuario")