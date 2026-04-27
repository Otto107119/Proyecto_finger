from app import db


class FactoresRiesgo(db.Model):
    __tablename__ = "factores_riesgo"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False,
        unique=True
    )

    alcohol = db.Column(db.Boolean, default=False)
    frecuencia_alcohol = db.Column(db.String(100), nullable=True)

    tabaco = db.Column(db.Boolean, default=False)
    frecuencia_tabaco = db.Column(db.String(100), nullable=True)

    drogas = db.Column(db.Boolean, default=False)
    frecuencia_drogas = db.Column(db.String(100), nullable=True)

    vida_sexual_activa = db.Column(db.Boolean, default=False)
    frecuencia_vida_sexual = db.Column(db.String(100), nullable=True)

    observaciones = db.Column(db.Text, nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "factores_riesgo",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )