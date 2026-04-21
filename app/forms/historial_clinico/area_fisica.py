from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional

class AreaFisicaForm(FlaskForm):
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

    submit = SubmitField("Guardar")