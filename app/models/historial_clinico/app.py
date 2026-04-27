from app import db


class APPResumen(db.Model):
    __tablename__ = "app_resumen"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False,
        unique=True
    )

    numero_embarazos = db.Column(db.String(50), nullable=True)
    farmacos_no_especificados = db.Column(db.Text, nullable=True)
    medicina_alterna = db.Column(db.Text, nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "app_resumen",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )


class APPPatologia(db.Model):
    __tablename__ = "app_patologia"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False
    )

    patologia = db.Column(db.String(255), nullable=True)
    hace_cuanto = db.Column(db.String(100), nullable=True)
    diagnostico = db.Column(db.String(255), nullable=True)
    farmaco = db.Column(db.String(255), nullable=True)
    dosis = db.Column(db.String(255), nullable=True)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "app_patologias",
            cascade="all, delete-orphan",
            lazy=True
        )
    )