from app import db
from datetime import datetime


class ActividadCognitiva(db.Model):
    __tablename__ = "actividad_cognitiva"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    paciente = db.relationship("Paciente", backref="actividades_cognitivas")
    
    fecha_evaluacion = db.Column(db.Date, default=datetime.utcnow)
    examinador = db.Column(db.String(150), nullable=True)

    edad = db.Column(db.Integer, nullable=True)
    sexo = db.Column(db.String(20), nullable=True)  # femenino / masculino
    escolaridad_anios = db.Column(db.Integer, nullable=True)
    idioma = db.Column(db.String(30), nullable=True, default="spanish")

    ocupacion = db.Column(db.String(150), nullable=True)
    preferencia_manual = db.Column(db.String(50), nullable=True)

    # =========================
    # MOCA
    # =========================
    moca_total = db.Column(db.Float, nullable=True)
    moca_z = db.Column(db.Float, nullable=True)
    moca_percentil = db.Column(db.Float, nullable=True)
    moca_estimacion = db.Column(db.String(100), nullable=True)

    # =========================
    # NUMBER SPAN / DÍGITOS
    # =========================
    digitos_directos_total = db.Column(db.Float, nullable=True)
    digitos_directos_longitud = db.Column(db.Float, nullable=True)

    digitos_inversos_total = db.Column(db.Float, nullable=True)
    digitos_inversos_longitud = db.Column(db.Float, nullable=True)

    digitos_directos_total_z = db.Column(db.Float, nullable=True)
    digitos_directos_total_percentil = db.Column(db.Float, nullable=True)

    digitos_directos_longitud_z = db.Column(db.Float, nullable=True)
    digitos_directos_longitud_percentil = db.Column(db.Float, nullable=True)

    digitos_inversos_total_z = db.Column(db.Float, nullable=True)
    digitos_inversos_total_percentil = db.Column(db.Float, nullable=True)

    digitos_inversos_longitud_z = db.Column(db.Float, nullable=True)
    digitos_inversos_longitud_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # TRAIL MAKING TEST
    # =========================
    trail_a_tiempo = db.Column(db.Float, nullable=True)
    trail_a_lineas_tiempo = db.Column(db.Float, nullable=True)

    trail_b_tiempo = db.Column(db.Float, nullable=True)
    trail_b_lineas_tiempo = db.Column(db.Float, nullable=True)

    trail_a_errores = db.Column(db.Integer, nullable=True)
    trail_b_errores = db.Column(db.Integer, nullable=True)

    trail_diferencial = db.Column(db.Float, nullable=True)
    trail_ratio = db.Column(db.Float, nullable=True)

    trail_a_z = db.Column(db.Float, nullable=True)
    trail_a_percentil = db.Column(db.Float, nullable=True)

    trail_b_z = db.Column(db.Float, nullable=True)
    trail_b_percentil = db.Column(db.Float, nullable=True)

    trail_diferencial_z = db.Column(db.Float, nullable=True)
    trail_diferencial_percentil = db.Column(db.Float, nullable=True)

    trail_ratio_z = db.Column(db.Float, nullable=True)
    trail_ratio_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # MINT-32
    # =========================
    mint_32_total = db.Column(db.Float, nullable=True)
    mint_32_z = db.Column(db.Float, nullable=True)
    mint_32_percentil = db.Column(db.Float, nullable=True)
    mint_32_estimacion = db.Column(db.String(100), nullable=True)

    # =========================
    # FLUENCIA FONOLÓGICA
    # =========================
    fluencia_p = db.Column(db.Float, nullable=True)
    fluencia_m = db.Column(db.Float, nullable=True)
    fluencia_pm_total = db.Column(db.Float, nullable=True)

    fluencia_p_z = db.Column(db.Float, nullable=True)
    fluencia_p_percentil = db.Column(db.Float, nullable=True)

    fluencia_m_z = db.Column(db.Float, nullable=True)
    fluencia_m_percentil = db.Column(db.Float, nullable=True)

    fluencia_pm_z = db.Column(db.Float, nullable=True)
    fluencia_pm_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # FLUIDEZ SEMÁNTICA
    # =========================
    fluidez_animales = db.Column(db.Float, nullable=True)
    fluidez_vegetales = db.Column(db.Float, nullable=True)

    fluidez_animales_z = db.Column(db.Float, nullable=True)
    fluidez_animales_percentil = db.Column(db.Float, nullable=True)

    fluidez_vegetales_z = db.Column(db.Float, nullable=True)
    fluidez_vegetales_percentil = db.Column(db.Float, nullable=True)

    fluencia_semantica_fonologica_diferencial = db.Column(db.Float, nullable=True)
    fluencia_semantica_fonologica_z = db.Column(db.Float, nullable=True)
    fluencia_semantica_fonologica_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # BENSON
    # =========================
    benson_copia_total = db.Column(db.Float, nullable=True)
    benson_recuerdo_total = db.Column(db.Float, nullable=True)
    benson_porcentaje_retenido = db.Column(db.Float, nullable=True)

    benson_copia_z = db.Column(db.Float, nullable=True)
    benson_copia_percentil = db.Column(db.Float, nullable=True)

    benson_recuerdo_z = db.Column(db.Float, nullable=True)
    benson_recuerdo_percentil = db.Column(db.Float, nullable=True)

    benson_retencion_z = db.Column(db.Float, nullable=True)
    benson_retencion_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # CRAFT STORY 21
    # =========================
    craft_inmediato_textual = db.Column(db.Float, nullable=True)
    craft_inmediato_parafraseo = db.Column(db.Float, nullable=True)

    craft_diferido_textual = db.Column(db.Float, nullable=True)
    craft_diferido_parafraseo = db.Column(db.Float, nullable=True)

    craft_porcentaje_retenido = db.Column(db.Float, nullable=True)

    craft_inmediato_textual_z = db.Column(db.Float, nullable=True)
    craft_inmediato_textual_percentil = db.Column(db.Float, nullable=True)

    craft_inmediato_parafraseo_z = db.Column(db.Float, nullable=True)
    craft_inmediato_parafraseo_percentil = db.Column(db.Float, nullable=True)

    craft_diferido_textual_z = db.Column(db.Float, nullable=True)
    craft_diferido_textual_percentil = db.Column(db.Float, nullable=True)

    craft_diferido_parafraseo_z = db.Column(db.Float, nullable=True)
    craft_diferido_parafraseo_percentil = db.Column(db.Float, nullable=True)

    craft_retencion_z = db.Column(db.Float, nullable=True)
    craft_retencion_percentil = db.Column(db.Float, nullable=True)

    # =========================
    # ÍNDICES GENERALES
    # =========================
    indice_errores = db.Column(db.Float, nullable=True)
    indice_errores_z = db.Column(db.Float, nullable=True)
    indice_errores_percentil = db.Column(db.Float, nullable=True)

    diferencia_retencion_verbal_visual = db.Column(db.Float, nullable=True)
    diferencia_retencion_verbal_visual_z = db.Column(db.Float, nullable=True)
    diferencia_retencion_verbal_visual_percentil = db.Column(db.Float, nullable=True)

    estimacion_global = db.Column(db.String(150), nullable=True)
    perfil_cognitivo = db.Column(db.Text, nullable=True)

    # =========================
    # SUEÑO
    # =========================
    sueno_indice_calidad = db.Column(db.Float, nullable=True)
    sueno_estimacion = db.Column(db.String(100), nullable=True)
    sueno_observaciones = db.Column(db.Text, nullable=True)

    # =========================
    # CONTROL DEL REGISTRO
    # =========================
    finalizado = db.Column(db.Boolean, default=False)

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )