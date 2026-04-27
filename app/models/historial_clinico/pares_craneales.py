from app import db

class ParesCraneales(db.Model):
    __tablename__ = "pares_craneales"

    id = db.Column(db.Integer, primary_key=True)

    historial_clinico_id = db.Column(
        db.Integer,
        db.ForeignKey("historial_clinico.id"),
        nullable=False,
        unique=True
    )

    evaluados = db.Column(db.Boolean, default=False)
    sin_alteraciones = db.Column(db.Boolean, default=False)
    alteraciones = db.Column(db.Text)
    observaciones_generales = db.Column(db.Text)

    dentadura_postiza = db.Column(db.Boolean, default=False)
    removible = db.Column(db.Boolean, default=False)
    piezas_perdidas = db.Column(db.Text)
    piezas_conservadas = db.Column(db.Text)
    piezas_fragiles = db.Column(db.Text)
    problemas_masticar = db.Column(db.Boolean, default=False)
    consistencia_alimentos = db.Column(db.String(20))
    atragantamientos = db.Column(db.Boolean, default=False)

    historial_clinico = db.relationship(
        "HistorialClinico",
        backref=db.backref(
            "pares_craneales",
            uselist=False,
            cascade="all, delete-orphan"
        )
    )