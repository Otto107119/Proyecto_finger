from datetime import datetime
from app import db


class ActividadNutricional(db.Model):
    __tablename__ = "actividad_nutricional"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo_comida = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(300))
    calorias = db.Column(db.Integer)
    observaciones = db.Column(db.String(300))

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="actividades_nutricionales")
    usuario = db.relationship("Usuario")