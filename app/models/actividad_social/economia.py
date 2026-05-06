from app import db


class ActividadSocialEconomia(db.Model):
    __tablename__ = "actividad_social_economia"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    ingreso_entrevistado = db.Column(db.Numeric(10, 2), default=0)
    otros_ingresos = db.Column(db.Numeric(10, 2), default=0)
    total_ingreso_mensual = db.Column(db.Numeric(10, 2), default=0)

    renta = db.Column(db.Numeric(10, 2), default=0)
    colegiaturas = db.Column(db.Numeric(10, 2), default=0)
    alimentacion = db.Column(db.Numeric(10, 2), default=0)
    gastos_medicos = db.Column(db.Numeric(10, 2), default=0)
    transporte = db.Column(db.Numeric(10, 2), default=0)
    diversion = db.Column(db.Numeric(10, 2), default=0)
    gasolina = db.Column(db.Numeric(10, 2), default=0)
    pagos_tarjetas = db.Column(db.Numeric(10, 2), default=0)
    luz = db.Column(db.Numeric(10, 2), default=0)
    ahorro = db.Column(db.Numeric(10, 2), default=0)
    agua = db.Column(db.Numeric(10, 2), default=0)
    deudas = db.Column(db.Numeric(10, 2), default=0)
    gas = db.Column(db.Numeric(10, 2), default=0)
    ropa = db.Column(db.Numeric(10, 2), default=0)
    telefono = db.Column(db.Numeric(10, 2), default=0)
    calzado = db.Column(db.Numeric(10, 2), default=0)
    telefono_celular = db.Column(db.Numeric(10, 2), default=0)
    alcohol_cigarros = db.Column(db.Numeric(10, 2), default=0)
    cable = db.Column(db.Numeric(10, 2), default=0)
    internet = db.Column(db.Numeric(10, 2), default=0)
    otros_gastos = db.Column(db.Numeric(10, 2), default=0)
    empleados_domesticos = db.Column(db.Numeric(10, 2), default=0)

    total_egresos = db.Column(db.Numeric(10, 2), default=0)
    balance_mensual = db.Column(db.Numeric(10, 2), default=0)

    actividad_social = db.relationship("ActividadSocial", back_populates="economia")

    def calcular_totales(self):
        self.total_ingreso_mensual = (self.ingreso_entrevistado or 0) + (self.otros_ingresos or 0)

        self.total_egresos = sum([
            self.renta or 0,
            self.colegiaturas or 0,
            self.alimentacion or 0,
            self.gastos_medicos or 0,
            self.transporte or 0,
            self.diversion or 0,
            self.gasolina or 0,
            self.pagos_tarjetas or 0,
            self.luz or 0,
            self.ahorro or 0,
            self.agua or 0,
            self.deudas or 0,
            self.gas or 0,
            self.ropa or 0,
            self.telefono or 0,
            self.calzado or 0,
            self.telefono_celular or 0,
            self.alcohol_cigarros or 0,
            self.cable or 0,
            self.internet or 0,
            self.otros_gastos or 0,
            self.empleados_domesticos or 0,
        ])

        self.balance_mensual = (self.total_ingreso_mensual or 0) - (self.total_egresos or 0)

    def __repr__(self):
        return f"<ActividadSocialEconomia actividad_social_id={self.actividad_social_id}>"