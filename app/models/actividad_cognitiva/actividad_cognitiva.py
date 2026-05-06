from datetime import datetime
from app import db


class ActividadCognitiva(db.Model):
    __tablename__ = "actividad_cognitiva"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(
    db.Integer,
    db.ForeignKey("paciente.id"),
    nullable=False
    )

    paciente = db.relationship(
        "Paciente",
        backref=db.backref(
            "actividades_cognitivas",
            cascade="all, delete-orphan",
            lazy=True
        )
    )

    fecha_evaluacion = db.Column(db.Date, nullable=True)
    examinador = db.Column(db.String(150), nullable=True)

    # Datos generales
    edad = db.Column(db.Integer, nullable=True)
    escolaridad_anios = db.Column(db.Integer, nullable=True)
    ocupacion = db.Column(db.String(150), nullable=True)
    preferencia_manual = db.Column(db.String(50), nullable=True)

    # Screening
    moca_total = db.Column(db.Integer, nullable=True)
    moca_estimacion = db.Column(db.String(100), nullable=True)

    # Atención
    digitos_directos_total = db.Column(db.Integer, nullable=True)
    digitos_directos_longitud = db.Column(db.Integer, nullable=True)
    digitos_inversos_total = db.Column(db.Integer, nullable=True)
    digitos_inversos_longitud = db.Column(db.Integer, nullable=True)

    # Atención sostenida
    trail_a_tiempo = db.Column(db.Float, nullable=True)
    trail_a_errores = db.Column(db.Integer, nullable=True)
    trail_a_lineas_correctas = db.Column(db.Integer, nullable=True)
    trail_a_estimacion = db.Column(db.String(100), nullable=True)

    # Flexibilidad cognitiva / función ejecutiva
    trail_b_tiempo = db.Column(db.Float, nullable=True)
    trail_b_errores = db.Column(db.Integer, nullable=True)
    trail_b_lineas_correctas = db.Column(db.Integer, nullable=True)
    trail_b_estimacion = db.Column(db.String(100), nullable=True)

    # Lenguaje / búsqueda léxica
    mint_32_total = db.Column(db.Integer, nullable=True)
    mint_32_estimacion = db.Column(db.String(100), nullable=True)

    # Fluencia fonológica
    fluencia_p = db.Column(db.Integer, nullable=True)
    fluencia_m = db.Column(db.Integer, nullable=True)
    fluencia_pm_promedio = db.Column(db.Float, nullable=True)
    fluencia_estimacion = db.Column(db.String(100), nullable=True)

    # Fluidez semántica
    animales_total = db.Column(db.Integer, nullable=True)
    vegetales_total = db.Column(db.Integer, nullable=True)
    fluidez_semantica_estimacion = db.Column(db.String(100), nullable=True)

    # Benson
    benson_inmediata = db.Column(db.Float, nullable=True)
    benson_diferida = db.Column(db.Float, nullable=True)
    benson_porcentaje_retenido = db.Column(db.Float, nullable=True)

    # Craft Story 21
    craft_ri_44 = db.Column(db.Integer, nullable=True)
    craft_ri_parafraseo_25 = db.Column(db.Integer, nullable=True)
    craft_rd_44 = db.Column(db.Integer, nullable=True)
    craft_rd_parafraseo_25 = db.Column(db.Integer, nullable=True)
    craft_porcentaje_retenido = db.Column(db.Float, nullable=True)

    # Índices derivados
    trail_puntuacion_diferencial = db.Column(db.Float, nullable=True)
    trail_puntuacion_ratio = db.Column(db.Float, nullable=True)
    diferencia_retencion_verbal_visual = db.Column(db.Float, nullable=True)

    # Resultado global
    resumen_automatico = db.Column(db.Text, nullable=True)
    estimacion_global = db.Column(db.String(100), nullable=True)

    finalizado = db.Column(db.Boolean, default=False)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
