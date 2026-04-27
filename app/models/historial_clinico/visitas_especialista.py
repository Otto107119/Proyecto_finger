from app import db


class VisitaEspecialista(db.Model):
    __tablename__ = "visita_especialista"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False
    )

    fecha_visita = db.Column(db.String(50), nullable=True)
    especialista = db.Column(db.String(255), nullable=True)
    motivo = db.Column(db.Text, nullable=True)
    tratamiento = db.Column(db.Text, nullable=True)
    estudios_requeridos = db.Column(db.Text, nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "visitas_especialista",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )