from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, SelectField, TextAreaField,
    BooleanField, DateField, SubmitField
)
from wtforms.validators import Optional


class HistorialClinicoForm(FlaskForm):
    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[Optional()])

    contacto_nombre = StringField("Nombre contacto 1", validators=[Optional()])
    contacto_telefono = StringField("Teléfono contacto 1", validators=[Optional()])
    contacto_nombre_2 = StringField("Nombre contacto 2", validators=[Optional()])
    contacto_telefono_2 = StringField("Teléfono contacto 2", validators=[Optional()])

    fuente_valoracion = SelectField(
        "Fuente de valoración",
        choices=[
            ("", "Seleccione"),
            ("Usuario", "Usuario"),
            ("Familiar", "Familiar"),
            ("Cuidador principal", "Cuidador principal")
        ],
        validators=[Optional()]
    )

    # Datos generales
    escolaridad = StringField("Escolaridad", validators=[Optional()])
    sabe_leer = BooleanField("Sabe leer")
    sabe_escribir = BooleanField("Sabe escribir")
    estado_civil = StringField("Estado civil", validators=[Optional()])
    ocupacion_anterior = StringField("Ocupación anterior", validators=[Optional()])
    ocupacion_actual = StringField("Ocupación actual", validators=[Optional()])
    domicilio_origen = TextAreaField("Domicilio de origen", validators=[Optional()])
    domicilio_actual = TextAreaField("Domicilio actual", validators=[Optional()])

    nucleo_procedencia = SelectField(
        "Núcleo de procedencia",
        choices=[("", "Seleccione"), ("Rural", "Rural"), ("Urbano", "Urbano")],
        validators=[Optional()]
    )

    vivienda = SelectField(
        "Vivienda",
        choices=[("", "Seleccione"), ("Propia", "Propia"), ("Rentada", "Rentada"), ("Prestada", "Prestada")],
        validators=[Optional()]
    )

    servicio_luz = BooleanField("Luz")
    servicio_agua = BooleanField("Agua")
    servicio_tel = BooleanField("Teléfono")
    servicio_internet = BooleanField("Internet")

    motivo_consulta = TextAreaField("Motivo de consulta", validators=[Optional()])

    # Área social
    tiene_hijos = BooleanField("Tiene hijos")
    hijas_mujeres = IntegerField("Mujeres", validators=[Optional()])
    hijos_hombres = IntegerField("Hombres", validators=[Optional()])
    vive_con = StringField("Vive con", validators=[Optional()])
    pension = BooleanField("Pensión")
    pension_cual = StringField("¿Cuál?", validators=[Optional()])
    ingreso_familiar_mensual = StringField("Monto de ingreso familiar al mes", validators=[Optional()])

    red_apoyo_amigos = BooleanField("Amigos")
    red_apoyo_familia = BooleanField("Familia")
    red_apoyo_vecinos = BooleanField("Vecinos")
    red_apoyo_nietos = BooleanField("Nietos")

    costumbres_tradiciones = TextAreaField("Costumbres y tradiciones", validators=[Optional()])
    actividades_gusta = TextAreaField("Actividades que le gusta realizar", validators=[Optional()])
    actividades_anteriores = TextAreaField("Actividades anteriores", validators=[Optional()])
    actividades_actuales = TextAreaField("Actividades actuales", validators=[Optional()])

    acude_taller = BooleanField("Acude a algún taller")
    taller_cual = StringField("¿Cuál taller?", validators=[Optional()])

    frecuencia_sale_semana = StringField("Frecuencia con la que sale de su casa por semana", validators=[Optional()])
    con_quien_sale = StringField("¿Con quién sale?", validators=[Optional()])

    cuidador = BooleanField("Cuidador")
    cuidador_quien = StringField("¿Quién?", validators=[Optional()])
    cuidador_remunerado = BooleanField("Remunerado")
    cuidador_antiguedad = StringField("Antigüedad", validators=[Optional()])
    cuidador_nombre = StringField("Nombre del cuidador", validators=[Optional()])
    cuidador_telefono = StringField("Teléfono del cuidador", validators=[Optional()])

    decide_asuntos_familiares = BooleanField("Decide asuntos familiares")
    relacion_familia = SelectField(
        "Relación con la familia",
        choices=[("", "Seleccione"), ("Buena", "Buena"), ("Mala", "Mala")],
        validators=[Optional()]
    )
    problemas_familiares = BooleanField("Problemas")
    tipo_problemas_familiares = StringField("Tipo de problema", validators=[Optional()])

    riesgos_entorno_social = TextAreaField("Riesgos en su entorno social", validators=[Optional()])
    medio_transporte_habitual = StringField("Medio de transporte habitual", validators=[Optional()])
    pasa_dia_con = StringField("Pasa el día con", validators=[Optional()])

    # Área espiritual
    sentido_vida = TextAreaField("Sentido de vida (¿Qué te motiva?)", validators=[Optional()])
    mision_vida = TextAreaField("Misión de su vida", validators=[Optional()])
    miedo_morir = BooleanField("Miedo a morir")
    piensa_muerte = TextAreaField("¿Qué piensa sobre la muerte?", validators=[Optional()])
    principales_miedos = TextAreaField("Principales miedos", validators=[Optional()])
    metas_vida = TextAreaField("Metas en su vida (¿Qué más quiere hacer?)", validators=[Optional()])

    # Área psicológica
    episodios_positivos = TextAreaField("Episodios positivos de su vida", validators=[Optional()])
    estado_animo = SelectField(
        "Estado de ánimo generalmente",
        choices=[
            ("", "Seleccione"),
            ("Feliz", "Feliz"),
            ("Triste", "Triste"),
            ("Angustia", "Angustia"),
            ("Otro", "Otro")
        ],
        validators=[Optional()]
    )
    estado_animo_otro = StringField("Otro estado de ánimo", validators=[Optional()])

    perdidas = BooleanField("Pérdidas")
    perdidas_cuales = TextAreaField("¿Cuáles?", validators=[Optional()])

    duelo = BooleanField("Duelo")
    duelo_tiempo = StringField("Tiempo", validators=[Optional()])
    tipo_duelo = StringField("Tipo de duelo", validators=[Optional()])

    estres = BooleanField("Estrés")
    afronta_estres = TextAreaField("¿Cómo lo afronta?", validators=[Optional()])

    ejercita_memoria = BooleanField("Ejercita su memoria")
    ejercita_memoria_como = TextAreaField("¿Cómo?", validators=[Optional()])

    olvidos_frecuentes = BooleanField("Olvidos frecuentes")
    olvidos_cuales = TextAreaField("¿Cuáles?", validators=[Optional()])

    satisfecho_vida = BooleanField("Satisfecho en su vida")
    satisfecho_vida_por_que = TextAreaField("¿Por qué?", validators=[Optional()])

    influye_opinion_demas = BooleanField("Influye la opinión de los demás en usted")
    influye_opinion_por_que = TextAreaField("¿Por qué?", validators=[Optional()])

    episodios_negativos = TextAreaField("Episodios negativos de su vida", validators=[Optional()])

    orientacion_persona = StringField("Persona", validators=[Optional()])
    orientacion_espacio = StringField("Espacio", validators=[Optional()])
    orientacion_tiempo = StringField("Tiempo", validators=[Optional()])
    orientacion_orientador = StringField("Orientador(a)", validators=[Optional()])

    comunicacion_verbal = TextAreaField("Comunicación verbal", validators=[Optional()])
    comunicacion_no_verbal = TextAreaField("Comunicación no verbal", validators=[Optional()])

    submit = SubmitField("Guardar")


    # Área física
    incontinencia = BooleanField("Incontinencia")
    incontinencia_urinaria = BooleanField("Urinaria")
    incontinencia_fecal = BooleanField("Fecal")
    panal = BooleanField("Pañal")

    estado_general = SelectField(
        "Estado general",
        choices=[
            ("", "Seleccione"),
            ("Bueno", "Bueno"),
            ("Regular", "Regular"),
            ("Malo", "Malo")
        ],
        validators=[Optional()]
    )

    biotipo = SelectField(
        "Biotipo",
        choices=[
            ("", "Seleccione"),
            ("Ectomorfo", "Ectomorfo"),
            ("Endomorfo", "Endomorfo"),
            ("Mesomorfo", "Mesomorfo")
        ],
        validators=[Optional()]
    )

    miembros_superiores = BooleanField("Miembros superiores")
    miembros_inferiores = BooleanField("Miembros inferiores")
    edema = BooleanField("Edema")

    deformidades = BooleanField("Deformidades")
    deformidades_localizacion = StringField("Localización de deformidades", validators=[Optional()])

    ulceras_vasculares = BooleanField("Úlceras vasculares")
    ulceras_vasculares_localizacion = StringField("Localización de úlceras vasculares", validators=[Optional()])

    ulceras_presion = BooleanField("Úlceras por presión")
    ulceras_presion_localizacion = StringField("Localización de úlceras por presión", validators=[Optional()])

    talla = StringField("Talla", validators=[Optional()])
    peso = StringField("Peso", validators=[Optional()])

    inmunizaciones = BooleanField("Inmunizaciones")
    inmunizaciones_cuales = TextAreaField("¿Cuáles inmunizaciones?", validators=[Optional()])

    miembros_amputados = BooleanField("Miembros amputados")
    miembros_amputados_cuales = StringField("¿Cuáles miembros amputados?", validators=[Optional()])

    horas_durmiendo = StringField("Horas durmiendo", validators=[Optional()])
    insomnio = BooleanField("Insomnio")

    cirugias = BooleanField("Cirugías")
    cirugias_nombre = StringField("Nombre de cirugía", validators=[Optional()])
    cirugias_anio = StringField("Año de cirugía", validators=[Optional()])

    antecedentes = BooleanField("Antecedentes")
    antecedentes_de_que = TextAreaField("¿Antecedentes de qué?", validators=[Optional()])

    acepta = BooleanField("Acepta")
    tipo_sangre = StringField("Tipo de sangre", validators=[Optional()])

    transfusiones = BooleanField("Transfusiones")
    transfusiones_cuales = TextAreaField("¿Cuáles transfusiones?", validators=[Optional()])

    alergias = BooleanField("Alergias")
    alergias_cuales = TextAreaField("¿Cuáles alergias?", validators=[Optional()])

    fc_max = StringField("FC Max (Frecuencia cardiaca máxima)", validators=[Optional()])
    temperatura_corporal = StringField("Temperatura corporal", validators=[Optional()])
    frecuencia_cardiaca = StringField("FC (Frecuencia cardiaca)", validators=[Optional()])
    frecuencia_respiratoria = StringField("FR (Frecuencia respiratoria)", validators=[Optional()])
    glucemia_capilar = StringField("Glucemia capilar", validators=[Optional()])
    tension_arterial = StringField("TA (Tensión arterial)", validators=[Optional()])

    actividad_fisica = BooleanField("Actividad física")



ESTADO_PAR_CHOICES = [
    ("", "Seleccione"),
    ("Normal", "Normal"),
    ("Alterado", "Alterado"),
    ("No valorado", "No valorado"),
]

CONSISTENCIA_CHOICES = [
    ("", "Seleccione"),
    ("Molido", "Molido"),
    ("Entero", "Entero"),
]

class ParesCranealesForm(FlaskForm):
    pc_i_estado = SelectField("I. Olfatorio", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_i_observacion = TextAreaField("Observación I", validators=[Optional()])

    pc_ii_estado = SelectField("II. Óptico", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_ii_observacion = TextAreaField("Observación II", validators=[Optional()])

    pc_iii_estado = SelectField("III. Motor ocular común", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_iii_observacion = TextAreaField("Observación III", validators=[Optional()])

    pc_iv_estado = SelectField("IV. Troclear", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_iv_observacion = TextAreaField("Observación IV", validators=[Optional()])

    pc_v_estado = SelectField("V. Trigémino", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_v_observacion = TextAreaField("Observación V", validators=[Optional()])

    pc_vi_estado = SelectField("VI. Abducens", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_vi_observacion = TextAreaField("Observación VI", validators=[Optional()])

    pc_vii_estado = SelectField("VII. Facial", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_vii_observacion = TextAreaField("Observación VII", validators=[Optional()])

    pc_viii_estado = SelectField("VIII. Vestibulococlear", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_viii_observacion = TextAreaField("Observación VIII", validators=[Optional()])

    pc_ix_estado = SelectField("IX. Glosofaríngeo", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_ix_observacion = TextAreaField("Observación IX", validators=[Optional()])

    pc_x_estado = SelectField("X. Vago", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_x_observacion = TextAreaField("Observación X", validators=[Optional()])

    pc_xi_estado = SelectField("XI. Accesorio", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_xi_observacion = TextAreaField("Observación XI", validators=[Optional()])

    pc_xii_estado = SelectField("XII. Hipogloso", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_xii_observacion = TextAreaField("Observación XII", validators=[Optional()])

    observaciones_generales = TextAreaField("Observaciones generales", validators=[Optional()])

    dentadura_postiza = BooleanField("Dentadura postiza")
    removible = BooleanField("Removible")
    piezas_perdidas = TextAreaField("Piezas perdidas", validators=[Optional()])
    piezas_conservadas = TextAreaField("Piezas conservadas", validators=[Optional()])
    piezas_fragiles = TextAreaField("Piezas frágiles", validators=[Optional()])
    problemas_masticar = BooleanField("Problemas al masticar")
    consistencia_alimentos = SelectField("Consistencia de alimentos", choices=CONSISTENCIA_CHOICES, validators=[Optional()])
    atragantamientos = BooleanField("Atragantamientos")

    submit = SubmitField("Guardar")