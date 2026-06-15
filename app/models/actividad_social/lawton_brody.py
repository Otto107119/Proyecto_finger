from datetime import datetime
from app import db


class ActividadSocialLawtonBrody(db.Model):
    __tablename__ = "actividad_social_lawton_brody"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    telefono = db.Column(db.Integer)
    transporte = db.Column(db.Integer)
    compras = db.Column(db.Integer)
    preparacion_alimentos = db.Column(db.Integer)
    quehaceres_hogar = db.Column(db.Integer)
    medicacion = db.Column(db.Integer)
    manejo_dinero = db.Column(db.Integer)

    puntaje_total = db.Column(db.Integer)
    interpretacion = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    actividad_social = db.relationship("ActividadSocial", back_populates="lawton_brody")