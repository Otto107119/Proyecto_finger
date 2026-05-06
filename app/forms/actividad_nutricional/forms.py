from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, FloatField, IntegerField, SelectField,
    TextAreaField, SubmitField
)
from wtforms.validators import Optional, NumberRange

class ActividadNutricionalForm(FlaskForm):

    problemas_masticacion_deglucion = BooleanField("Problemas de masticación o deglución")
    alergias_alimentos = BooleanField("Alergias a alimentos")
    intolerancias_alimentos = BooleanField("Intolerancias a alimentos")

    peso = FloatField("Peso en kg", validators=[Optional(), NumberRange(min=0)])
    talla = FloatField("Talla en cm", validators=[Optional(), NumberRange(min=0)])
    cintura = FloatField("Circunferencia de cintura en cm", validators=[Optional()])
    cadera = FloatField("Circunferencia de cadera en cm", validators=[Optional()])
    pantorrilla = FloatField("Circunferencia de pantorrilla en cm", validators=[Optional()])

    frutas_diarias = BooleanField("¿Consume frutas diariamente?")
    verduras_diarias = BooleanField("¿Consume verduras diariamente?")
    leguminosas = BooleanField("¿Incluye leguminosas 3 o más veces por semana?")
    proteina_adecuada = BooleanField("¿Consume proteína adecuada diariamente?")
    cereales_integrales = BooleanField("¿Prefiere cereales integrales?")
    limita_refrescos_jugos = BooleanField("¿Limita refrescos y jugos?")
    limita_embutidos_procesados = BooleanField("¿Limita embutidos y procesados?")
    agua_suficiente = BooleanField("¿Consume 1.5 L o más de agua al día?")
    grasas_saludables = BooleanField("¿Incluye grasas saludables?")
    mas_de_tres_comidas = BooleanField("¿Realiza más de 3 tiempos de comida?")

    mna_ingesta = SelectField(
        "Disminución de ingesta",
        choices=[
            ("", "Seleccione"),
            ("0", "Disminución severa"),
            ("1", "Disminución moderada"),
            ("2", "Sin disminución"),
        ],
        validators=[Optional()]
    )

    mna_perdida_peso = SelectField(
        "Pérdida de peso en los últimos 3 meses",
        choices=[
            ("", "Seleccione"),
            ("0", "Pérdida mayor de 3 kg"),
            ("1", "No lo sabe"),
            ("2", "Pérdida entre 1 y 3 kg"),
            ("3", "Sin pérdida de peso"),
        ],
        validators=[Optional()]
    )

    mna_movilidad = SelectField(
        "Movilidad",
        choices=[
            ("", "Seleccione"),
            ("0", "Postrado en cama o silla"),
            ("1", "Puede levantarse pero no sale"),
            ("2", "Sale de casa"),
        ],
        validators=[Optional()]
    )

    mna_estres = SelectField(
        "Estrés psicológico o enfermedad aguda",
        choices=[
            ("", "Seleccione"),
            ("0", "Sí"),
            ("2", "No"),
        ],
        validators=[Optional()]
    )

    mna_neuropsicologicos = SelectField(
        "Problemas neuropsicológicos",
        choices=[
            ("", "Seleccione"),
            ("0", "Demencia o depresión severa"),
            ("1", "Demencia leve"),
            ("2", "Sin problemas psicológicos"),
        ],
        validators=[Optional()]
    )

    mna_imc = SelectField(
        "IMC / Pantorrilla",
        choices=[
            ("", "Seleccione"),
            ("0", "IMC < 19 o pantorrilla < 31 cm"),
            ("1", "IMC 19 - <21"),
            ("2", "IMC 21 - <23"),
            ("3", "IMC ≥ 23 o pantorrilla ≥ 31 cm"),
        ],
        validators=[Optional()]
    )

    dia_recordatorio = SelectField(
        "Día del recordatorio de 24 horas",
        choices=[
            ("", "Seleccione"),
            ("Lunes", "Lunes"),
            ("Martes", "Martes"),
            ("Miércoles", "Miércoles"),
            ("Jueves", "Jueves"),
            ("Viernes", "Viernes"),
            ("Sábado", "Sábado"),
            ("Domingo", "Domingo"),
        ],
        validators=[Optional()]
    )

    observaciones = TextAreaField("Observaciones", validators=[Optional()])
    
    # -------- DESAYUNO --------
    desayuno_frutas = IntegerField("Frutas", default=0)
    desayuno_verduras = IntegerField("Verduras", default=0)
    desayuno_cereales = IntegerField("Cereales", default=0)
    desayuno_lacteos = IntegerField("Lácteos", default=0)
    desayuno_leguminosas = IntegerField("Leguminosas", default=0)
    desayuno_aoa = IntegerField("AOA", default=0)
    desayuno_aceites = IntegerField("Aceites y grasas", default=0)
    desayuno_cafe = IntegerField("Café", default=0)
    desayuno_azucar = IntegerField("Azúcar", default=0)

    # -------- COMIDA --------
    comida_frutas = IntegerField("Frutas", default=0)
    comida_verduras = IntegerField("Verduras", default=0)
    comida_cereales = IntegerField("Cereales", default=0)
    comida_leguminosas = IntegerField("Leguminosas", default=0)
    comida_aoa = IntegerField("AOA", default=0)
    comida_aceites = IntegerField("Aceites y grasas", default=0)

    # -------- INTERMEDIOS --------
    intermedio_frutas = IntegerField("Frutas", default=0)
    intermedio_verduras = IntegerField("Verduras", default=0)
    intermedio_cereales = IntegerField("Cereales", default=0)
    intermedio_lacteos = IntegerField("Lácteos", default=0)
    intermedio_frutos_secos = IntegerField("Frutos secos", default=0)

    # -------- CENA --------
    cena_frutas = IntegerField("Frutas", default=0)
    cena_verduras = IntegerField("Verduras", default=0)
    cena_cereales = IntegerField("Cereales", default=0)
    cena_lacteos = IntegerField("Lácteos", default=0)
    cena_leguminosas = IntegerField("Leguminosas", default=0)
    cena_aoa = IntegerField("AOA", default=0)
    cena_aceites = IntegerField("Aceites y grasas", default=0)

    submit = SubmitField("Guardar actividad nutricional")
