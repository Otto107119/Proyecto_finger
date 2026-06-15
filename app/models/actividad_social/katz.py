from datetime import datetime
from app import db


class ActividadSocialKatz(db.Model):
    __tablename__ = "actividad_social_katz"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    bano = db.Column(db.Integer)
    vestido = db.Column(db.Integer)
    uso_sanitario = db.Column(db.Integer)
    transferencias = db.Column(db.Integer)
    continencia = db.Column(db.Integer)
    alimentacion = db.Column(db.Integer)

    puntaje_total = db.Column(db.Integer)
    clasificacion_letra = db.Column(db.String(5))
    interpretacion = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    actividad_social = db.relationship("ActividadSocial", back_populates="katz")