from datetime import datetime
from app import db


class ActividadSocial(db.Model):
    __tablename__ = "actividad_social"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(
        db.Integer,
        db.ForeignKey("paciente.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    seguridad_social = db.Column(db.String(20), nullable=True)
    tiempo_residencia_ameca = db.Column(db.Integer, nullable=True)
    tipo_vivienda = db.Column(db.String(20), nullable=True)
    migracion = db.Column(db.Boolean, default=False, nullable=False)
    observaciones = db.Column(db.Text, nullable=True)
    
    finalizado = db.Column(db.Boolean, default=False, nullable=False)
    fecha_finalizado = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    paciente = db.relationship("Paciente", back_populates="actividad_social")

    economia = db.relationship(
        "ActividadSocialEconomia",
        back_populates="actividad_social",
        uselist=False,
        cascade="all, delete-orphan"
    )

    padres = db.relationship(
        "ActividadSocialPadreMadre",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )

    hermanos = db.relationship(
        "ActividadSocialHermano",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )

    hijos = db.relationship(
        "ActividadSocialHijo",
        back_populates="actividad_social",
        cascade="all, delete-orphan"
    )
    
    

    def __repr__(self):
        return f"<ActividadSocial paciente_id={self.paciente_id}>"
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
class ActividadSocialPadreMadre(db.Model):
    __tablename__ = "actividad_social_padres_madres"

    id = db.Column(db.Integer, primary_key=True)
    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    tipo = db.Column(db.String(10), nullable=False)  # padre / madre
    nombre = db.Column(db.String(150), nullable=True)
    edad_o_tiempo_vida = db.Column(db.Integer, nullable=True)
    vive = db.Column(db.Boolean, default=True, nullable=False)
    causa_muerte = db.Column(db.String(50), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)

    actividad_social = db.relationship("ActividadSocial", back_populates="padres")

    def __repr__(self):
        return f"<ActividadSocialPadreMadre tipo={self.tipo} nombre={self.nombre}>"
class ActividadSocialHermano(db.Model):
    __tablename__ = "actividad_social_hermanos"

    id = db.Column(db.Integer, primary_key=True)
    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    relacion = db.Column(db.String(20), nullable=True)
    donde_vive = db.Column(db.String(150), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)

    actividad_social = db.relationship("ActividadSocial", back_populates="hermanos")

    def __repr__(self):
        return f"<ActividadSocialHermano nombre={self.nombre}>"

class ActividadSocialHijo(db.Model):
    __tablename__ = "actividad_social_hijos"

    id = db.Column(db.Integer, primary_key=True)

    actividad_social_id = db.Column(
        db.Integer,
        db.ForeignKey("actividad_social.id", ondelete="CASCADE"),
        nullable=False
    )

    nombre = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    estado_civil = db.Column(db.String(20), nullable=True)
    relacion = db.Column(db.String(20), nullable=True)
    donde_vive = db.Column(db.String(150), nullable=True)
    enfermedad = db.Column(db.String(150), nullable=True)
    numero_hijos = db.Column(db.Integer, nullable=True)

    actividad_social = db.relationship(
        "ActividadSocial",
        back_populates="hijos"
    )

    def __repr__(self):
        return f"<ActividadSocialHijo nombre={self.nombre}>"
    