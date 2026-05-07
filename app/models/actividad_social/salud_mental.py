from app import db


class ActividadSocialSaludMental(db.Model):
    __tablename__ = "actividad_social_salud_mental"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # GDS 15
    gds_total = db.Column(db.Integer, nullable=True)
    gds_interpretacion = db.Column(db.String(50), nullable=True)

    # Lawton y Brody
    lawton_telefono = db.Column(db.String(1), nullable=True)
    lawton_transporte = db.Column(db.String(1), nullable=True)
    lawton_compras = db.Column(db.String(1), nullable=True)
    lawton_alimentos = db.Column(db.String(1), nullable=True)
    lawton_hogar = db.Column(db.String(1), nullable=True)
    lawton_medicacion = db.Column(db.String(1), nullable=True)
    lawton_dinero = db.Column(db.String(1), nullable=True)

    # Katz
    katz_banio = db.Column(db.String(1), nullable=True)
    katz_vestido = db.Column(db.String(1), nullable=True)
    katz_sanitario = db.Column(db.String(1), nullable=True)
    katz_transferencia = db.Column(db.String(1), nullable=True)
    katz_continencia = db.Column(db.String(1), nullable=True)
    katz_alimentacion = db.Column(db.String(1), nullable=True)

    katz_total = db.Column(db.Integer, nullable=True)
    katz_letra = db.Column(db.String(5), nullable=True)
    katz_interpretacion = db.Column(db.String(100), nullable=True)

    actividad_social = db.relationship(
        "ActividadSocial",
        back_populates="salud_mental"
    )

    def __repr__(self):
        return f"<ActividadSocialSaludMental actividad_social_id={self.actividad_social_id}>"