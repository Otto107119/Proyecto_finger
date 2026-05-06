from app import db
from datetime import datetime


class ActividadNutricional(db.Model):
    __tablename__ = "actividad_nutricional"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)

    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # Datos generales
    problemas_masticacion_deglucion = db.Column(db.Boolean, default=False)
    alergias_alimentos = db.Column(db.Boolean, default=False)
    intolerancias_alimentos = db.Column(db.Boolean, default=False)

    peso = db.Column(db.Float)
    talla = db.Column(db.Float)
    cintura = db.Column(db.Float)
    cadera = db.Column(db.Float)
    pantorrilla = db.Column(db.Float)

    imc = db.Column(db.Float)

    # Índice de calidad de dieta
    frutas_diarias = db.Column(db.Boolean, default=False)
    verduras_diarias = db.Column(db.Boolean, default=False)
    leguminosas = db.Column(db.Boolean, default=False)
    proteina_adecuada = db.Column(db.Boolean, default=False)
    cereales_integrales = db.Column(db.Boolean, default=False)
    limita_refrescos_jugos = db.Column(db.Boolean, default=False)
    limita_embutidos_procesados = db.Column(db.Boolean, default=False)
    agua_suficiente = db.Column(db.Boolean, default=False)
    grasas_saludables = db.Column(db.Boolean, default=False)
    mas_de_tres_comidas = db.Column(db.Boolean, default=False)

    puntaje_calidad_dieta = db.Column(db.Integer)
    interpretacion_calidad_dieta = db.Column(db.String(100))

    # MNA-SF
    mna_ingesta = db.Column(db.Integer)
    mna_perdida_peso = db.Column(db.Integer)
    mna_movilidad = db.Column(db.Integer)
    mna_estres = db.Column(db.Integer)
    mna_neuropsicologicos = db.Column(db.Integer)
    mna_imc = db.Column(db.Integer)

    puntaje_mna = db.Column(db.Integer)
    interpretacion_mna = db.Column(db.String(100))

    # Recordatorio 24 horas
    dia_recordatorio = db.Column(db.String(20))

    observaciones = db.Column(db.Text)

    paciente = db.relationship(
        "Paciente",
        backref=db.backref(
            "actividades_nutricionales",
            cascade="all, delete-orphan",
            lazy=True
        )
    )

class RecordatorioNutricional(db.Model):
    __tablename__ = "recordatorio_nutricional"

    id = db.Column(db.Integer, primary_key=True)
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad_nutricional.id"), nullable=False)

    tiempo_comida = db.Column(db.String(50))  # desayuno, comida, intermedio, cena
    frutas = db.Column(db.Integer, default=0)
    verduras = db.Column(db.Integer, default=0)
    cereales = db.Column(db.Integer, default=0)
    lacteos = db.Column(db.Integer, default=0)
    leguminosas = db.Column(db.Integer, default=0)
    aoa = db.Column(db.Integer, default=0)
    aceites_grasas = db.Column(db.Integer, default=0)
    cafe = db.Column(db.Integer, default=0)
    azucar = db.Column(db.Integer, default=0)
    frutos_secos = db.Column(db.Integer, default=0)

    actividad = db.relationship(
        "ActividadNutricional",
        backref=db.backref("recordatorios", cascade="all, delete-orphan")
    )


class FrecuenciaGrasas(db.Model):
    __tablename__ = "frecuencia_grasas"

    id = db.Column(db.Integer, primary_key=True)
    actividad_id = db.Column(db.Integer, db.ForeignKey("actividad_nutricional.id"), nullable=False)

    tipo_grasa = db.Column(db.String(100))
    utiliza = db.Column(db.Boolean, default=False)
    frecuencia = db.Column(db.String(50))

    actividad = db.relationship(
        "ActividadNutricional",
        backref=db.backref("frecuencia_grasas", cascade="all, delete-orphan")
    )