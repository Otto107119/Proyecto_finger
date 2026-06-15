from datetime import datetime
from app import db


class ActividadSocialGDS15(db.Model):
    __tablename__ = "actividad_social_gds15"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    p1 = db.Column(db.String(2))
    p2 = db.Column(db.String(2))
    p3 = db.Column(db.String(2))
    p4 = db.Column(db.String(2))
    p5 = db.Column(db.String(2))
    p6 = db.Column(db.String(2))
    p7 = db.Column(db.String(2))
    p8 = db.Column(db.String(2))
    p9 = db.Column(db.String(2))
    p10 = db.Column(db.String(2))
    p11 = db.Column(db.String(2))
    p12 = db.Column(db.String(2))
    p13 = db.Column(db.String(2))
    p14 = db.Column(db.String(2))
    p15 = db.Column(db.String(2))

    puntaje_total = db.Column(db.Integer)
    interpretacion = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    actividad_social = db.relationship("ActividadSocial", back_populates="gds15")