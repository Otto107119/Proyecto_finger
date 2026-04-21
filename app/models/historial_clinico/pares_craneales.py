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

    pc_i_estado = db.Column(db.String(20))
    pc_i_observacion = db.Column(db.Text)

    pc_ii_estado = db.Column(db.String(20))
    pc_ii_observacion = db.Column(db.Text)

    pc_iii_estado = db.Column(db.String(20))
    pc_iii_observacion = db.Column(db.Text)

    pc_iv_estado = db.Column(db.String(20))
    pc_iv_observacion = db.Column(db.Text)

    pc_v_estado = db.Column(db.String(20))
    pc_v_observacion = db.Column(db.Text)

    pc_vi_estado = db.Column(db.String(20))
    pc_vi_observacion = db.Column(db.Text)

    pc_vii_estado = db.Column(db.String(20))
    pc_vii_observacion = db.Column(db.Text)

    pc_viii_estado = db.Column(db.String(20))
    pc_viii_observacion = db.Column(db.Text)

    pc_ix_estado = db.Column(db.String(20))
    pc_ix_observacion = db.Column(db.Text)

    pc_x_estado = db.Column(db.String(20))
    pc_x_observacion = db.Column(db.Text)

    pc_xi_estado = db.Column(db.String(20))
    pc_xi_observacion = db.Column(db.Text)

    pc_xii_estado = db.Column(db.String(20))
    pc_xii_observacion = db.Column(db.Text)

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
        backref=db.backref("pares_craneales", uselist=False, cascade="all, delete-orphan")
    )