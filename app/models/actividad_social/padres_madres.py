from app import db


class ActividadSocialPadreMadre(db.Model):
    __tablename__ = "actividad_social_padres_madres"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    tipo = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(150), nullable=True)
    edad_o_tiempo_vida = db.Column(db.Integer, nullable=True)
    vive = db.Column(db.Boolean, default=True, nullable=False)
    causa_muerte = db.Column(db.String(50), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)

    actividad_social = db.relationship("ActividadSocial", back_populates="padres")

    def __repr__(self):
        return f"<ActividadSocialPadreMadre tipo={self.tipo} nombre={self.nombre}>"