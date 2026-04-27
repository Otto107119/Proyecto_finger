from app import db


class EstudioComplementario(db.Model):
    __tablename__ = "estudio_complementario"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False
    )

    estudio = db.Column(db.String(255), nullable=True)
    resultado = db.Column(db.Text, nullable=True)
    tratamiento = db.Column(db.Text, nullable=True)
    fecha_estudio = db.Column(db.String(50), nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "estudios_complementarios",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )