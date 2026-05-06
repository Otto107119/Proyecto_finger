from app import db
from datetime import datetime


class AreaMedica(db.Model):
    __tablename__ = "area_medica"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Riesgo cardiovascular
    sexo = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    presion_sistolica = db.Column(db.Float)

    tratamiento_hipertension = db.Column(db.Boolean, default=False)
    fumador = db.Column(db.Boolean, default=False)
    diabetico = db.Column(db.Boolean, default=False)

    hdl = db.Column(db.Float)
    colesterol = db.Column(db.Float)

    edad_corazon = db.Column(db.Float)
    porcentaje_riesgo = db.Column(db.Float)
    interpretacion_riesgo = db.Column(db.String(100))

    # Laboratoriales - perfil lipídico
    colesterol_total = db.Column(db.Float)
    colesterol_ldl = db.Column(db.Float)
    colesterol_hdl = db.Column(db.Float)
    trigliceridos = db.Column(db.Float)

    # Glucosa
    glucosa_capilar = db.Column(db.Float)

    paciente = db.relationship(
        "Paciente",
        backref=db.backref(
            "areas_medicas",
            cascade="all, delete-orphan",
            lazy=True
        )
    )