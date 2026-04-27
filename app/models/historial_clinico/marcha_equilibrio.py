from app import db


class MarchaEquilibrio(db.Model):
    __tablename__ = "marcha_equilibrio"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False,
        unique=True
    )

    cifosis = db.Column(db.Boolean, default=False)
    lordosis = db.Column(db.Boolean, default=False)
    escoliosis = db.Column(db.Boolean, default=False)

    mareos = db.Column(db.Boolean, default=False)
    sincope = db.Column(db.Boolean, default=False)

    caidas = db.Column(db.Boolean, default=False)
    frecuencia_caidas = db.Column(db.String(100), nullable=True)

    fracturas = db.Column(db.Boolean, default=False)
    antiguedad_fracturas = db.Column(db.String(100), nullable=True)

    consecuencias_secuelas = db.Column(db.Text, nullable=True)
    ayudas_tecnicas = db.Column(db.Text, nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "marcha_equilibrio",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )