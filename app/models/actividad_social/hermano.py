from app import db


class ActividadSocialHermano(db.Model):
    __tablename__ = "actividad_social_hermanos"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    relacion = db.Column(db.String(20), nullable=True)
    donde_vive = db.Column(db.String(150), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)

    actividad_social = db.relationship("ActividadSocial", back_populates="hermanos")

    def __repr__(self):
        return f"<ActividadSocialHermano nombre={self.nombre}>"