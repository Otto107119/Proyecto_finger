from datetime import datetime
from app import db


class HistorialClinico(db.Model):
    __tablename__ = "historial_clinico"

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey("paciente.id"), nullable=False)
    paciente = db.relationship("Paciente", backref="historiales_clinicos")

    fecha = db.Column(db.Date, nullable=True)

    # Encabezado
    contacto_nombre = db.Column(db.String(150), nullable=True)
    contacto_telefono = db.Column(db.String(30), nullable=True)
    contacto_nombre_2 = db.Column(db.String(150), nullable=True)
    contacto_telefono_2 = db.Column(db.String(30), nullable=True)
    fuente_valoracion = db.Column(db.String(50), nullable=True)

    # Datos generales
    escolaridad = db.Column(db.String(100), nullable=True)
    sabe_leer = db.Column(db.Boolean, default=False)
    sabe_escribir = db.Column(db.Boolean, default=False)
    estado_civil = db.Column(db.String(50), nullable=True)
    ocupacion_anterior = db.Column(db.String(150), nullable=True)
    ocupacion_actual = db.Column(db.String(150), nullable=True)
    domicilio_origen = db.Column(db.Text, nullable=True)
    domicilio_actual = db.Column(db.Text, nullable=True)
    nucleo_procedencia = db.Column(db.String(20), nullable=True)
    vivienda = db.Column(db.String(20), nullable=True)

    servicio_luz = db.Column(db.Boolean, default=False)
    servicio_agua = db.Column(db.Boolean, default=False)
    servicio_tel = db.Column(db.Boolean, default=False)
    servicio_internet = db.Column(db.Boolean, default=False)

    motivo_consulta = db.Column(db.Text, nullable=True)

    # Área social
    tiene_hijos = db.Column(db.Boolean, default=False)
    hijas_mujeres = db.Column(db.Integer, nullable=True)
    hijos_hombres = db.Column(db.Integer, nullable=True)
    vive_con = db.Column(db.String(150), nullable=True)
    pension = db.Column(db.Boolean, default=False)
    pension_cual = db.Column(db.String(150), nullable=True)
    ingreso_familiar_mensual = db.Column(db.String(100), nullable=True)
    red_apoyo_amigos = db.Column(db.Boolean, default=False)
    red_apoyo_familia = db.Column(db.Boolean, default=False)
    red_apoyo_vecinos = db.Column(db.Boolean, default=False)
    red_apoyo_nietos = db.Column(db.Boolean, default=False)
    costumbres_tradiciones = db.Column(db.Text, nullable=True)
    actividades_gusta = db.Column(db.Text, nullable=True)
    actividades_anteriores = db.Column(db.Text, nullable=True)
    actividades_actuales = db.Column(db.Text, nullable=True)
    acude_taller = db.Column(db.Boolean, default=False)
    taller_cual = db.Column(db.String(150), nullable=True)
    frecuencia_sale_semana = db.Column(db.String(100), nullable=True)
    con_quien_sale = db.Column(db.String(150), nullable=True)
    cuidador = db.Column(db.Boolean, default=False)
    cuidador_quien = db.Column(db.String(150), nullable=True)
    cuidador_remunerado = db.Column(db.Boolean, default=False)
    cuidador_antiguedad = db.Column(db.String(100), nullable=True)
    cuidador_nombre = db.Column(db.String(150), nullable=True)
    cuidador_telefono = db.Column(db.String(30), nullable=True)
    decide_asuntos_familiares = db.Column(db.Boolean, default=False)
    relacion_familia = db.Column(db.String(20), nullable=True)
    problemas_familiares = db.Column(db.Boolean, default=False)
    tipo_problemas_familiares = db.Column(db.String(200), nullable=True)
    riesgos_entorno_social = db.Column(db.Text, nullable=True)
    medio_transporte_habitual = db.Column(db.String(150), nullable=True)
    pasa_dia_con = db.Column(db.String(150), nullable=True)

    # Área espiritual
    sentido_vida = db.Column(db.Text, nullable=True)
    mision_vida = db.Column(db.Text, nullable=True)
    miedo_morir = db.Column(db.Boolean, default=False)
    piensa_muerte = db.Column(db.Text, nullable=True)
    principales_miedos = db.Column(db.Text, nullable=True)
    metas_vida = db.Column(db.Text, nullable=True)

    # Área psicológica
    episodios_positivos = db.Column(db.Text, nullable=True)
    estado_animo = db.Column(db.String(50), nullable=True)
    estado_animo_otro = db.Column(db.String(100), nullable=True)
    perdidas = db.Column(db.Boolean, default=False)
    perdidas_cuales = db.Column(db.Text, nullable=True)
    duelo = db.Column(db.Boolean, default=False)
    duelo_tiempo = db.Column(db.String(100), nullable=True)
    tipo_duelo = db.Column(db.String(150), nullable=True)
    estres = db.Column(db.Boolean, default=False)
    afronta_estres = db.Column(db.Text, nullable=True)
    ejercita_memoria = db.Column(db.Boolean, default=False)
    ejercita_memoria_como = db.Column(db.Text, nullable=True)
    olvidos_frecuentes = db.Column(db.Boolean, default=False)
    olvidos_cuales = db.Column(db.Text, nullable=True)
    satisfecho_vida = db.Column(db.Boolean, default=False)
    satisfecho_vida_por_que = db.Column(db.Text, nullable=True)
    influye_opinion_demas = db.Column(db.Boolean, default=False)
    influye_opinion_por_que = db.Column(db.Text, nullable=True)
    episodios_negativos = db.Column(db.Text, nullable=True)
    orientacion_persona = db.Column(db.String(150), nullable=True)
    orientacion_espacio = db.Column(db.String(150), nullable=True)
    orientacion_tiempo = db.Column(db.String(150), nullable=True)
    orientacion_orientador = db.Column(db.String(150), nullable=True)
    comunicacion_verbal = db.Column(db.Text, nullable=True)
    comunicacion_no_verbal = db.Column(db.Text, nullable=True)

    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    # Área física
    incontinencia = db.Column(db.Boolean, default=False)
    incontinencia_urinaria = db.Column(db.Boolean, default=False)
    incontinencia_fecal = db.Column(db.Boolean, default=False)
    panal = db.Column(db.Boolean, default=False)

    estado_general = db.Column(db.String(20), nullable=True)
    biotipo = db.Column(db.String(20), nullable=True)

    miembros_superiores = db.Column(db.Boolean, default=False)
    miembros_inferiores = db.Column(db.Boolean, default=False)
    edema = db.Column(db.Boolean, default=False)

    deformidades = db.Column(db.Boolean, default=False)
    deformidades_localizacion = db.Column(db.String(255), nullable=True)

    ulceras_vasculares = db.Column(db.Boolean, default=False)
    ulceras_vasculares_localizacion = db.Column(db.String(255), nullable=True)

    ulceras_presion = db.Column(db.Boolean, default=False)
    ulceras_presion_localizacion = db.Column(db.String(255), nullable=True)

    talla = db.Column(db.String(50), nullable=True)
    peso = db.Column(db.String(50), nullable=True)

    inmunizaciones = db.Column(db.Boolean, default=False)
    inmunizaciones_cuales = db.Column(db.Text, nullable=True)

    miembros_amputados = db.Column(db.Boolean, default=False)
    miembros_amputados_cuales = db.Column(db.String(255), nullable=True)

    horas_durmiendo = db.Column(db.String(50), nullable=True)
    insomnio = db.Column(db.Boolean, default=False)

    cirugias = db.Column(db.Boolean, default=False)
    cirugias_nombre = db.Column(db.String(255), nullable=True)
    cirugias_anio = db.Column(db.String(50), nullable=True)

    antecedentes = db.Column(db.Boolean, default=False)
    antecedentes_de_que = db.Column(db.Text, nullable=True)

    acepta = db.Column(db.Boolean, default=False)
    tipo_sangre = db.Column(db.String(20), nullable=True)

    transfusiones = db.Column(db.Boolean, default=False)
    transfusiones_cuales = db.Column(db.Text, nullable=True)

    alergias = db.Column(db.Boolean, default=False)
    alergias_cuales = db.Column(db.Text, nullable=True)

    fc_max = db.Column(db.String(50), nullable=True)
    temperatura_corporal = db.Column(db.String(50), nullable=True)
    frecuencia_cardiaca = db.Column(db.String(50), nullable=True)
    frecuencia_respiratoria = db.Column(db.String(50), nullable=True)
    glucemia_capilar = db.Column(db.String(50), nullable=True)
    tension_arterial = db.Column(db.String(50), nullable=True)

    actividad_fisica = db.Column(db.Boolean, default=False)