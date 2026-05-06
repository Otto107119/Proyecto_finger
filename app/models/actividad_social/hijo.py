from app import db


class ActividadSocialHijo(db.Model):
    __tablename__ = "actividad_social_hijos"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    estado_civil = db.Column(db.String(20), nullable=True)
    relacion = db.Column(db.String(20), nullable=True)
    donde_vive = db.Column(db.String(150), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)
    numero_hijos = db.Column(db.Integer, nullable=True)

    actividad_social = db.relationship(
        "ActividadSocial",
        back_populates="hijos"
    )

    def __repr__(self):
        return f"<ActividadSocialHijo nombre={self.nombre}>"