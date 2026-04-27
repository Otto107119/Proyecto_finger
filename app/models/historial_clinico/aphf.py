from app import db


class APHF(db.Model):
    __tablename__ = "aphf"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False,
        unique=True
    )

    vive_padre = db.Column(db.Boolean, default=False)
    edad_padre = db.Column(db.String(50), nullable=True)
    padecimientos_padre = db.Column(db.Text, nullable=True)

    vive_madre = db.Column(db.Boolean, default=False)
    edad_madre = db.Column(db.String(50), nullable=True)
    padecimientos_madre = db.Column(db.Text, nullable=True)

    numero_hermanos = db.Column(db.String(50), nullable=True)
    padecimientos_hermanos = db.Column(db.Text, nullable=True)

    numero_hijos = db.Column(db.String(50), nullable=True)
    padecimientos_hijos = db.Column(db.Text, nullable=True)

    diabetes = db.Column(db.Boolean, default=False)
    hipertension = db.Column(db.Boolean, default=False)
    cancer = db.Column(db.Boolean, default=False)
    cardiopatias = db.Column(db.Boolean, default=False)
    obesidad = db.Column(db.Boolean, default=False)
    demencia = db.Column(db.Boolean, default=False)
    alzheimer = db.Column(db.Boolean, default=False)
    parkinson = db.Column(db.Boolean, default=False)
    enfermedad_renal = db.Column(db.Boolean, default=False)

    otra_enfermedad = db.Column(db.String(255), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "aphf",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )