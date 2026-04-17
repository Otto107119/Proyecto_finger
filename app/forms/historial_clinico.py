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