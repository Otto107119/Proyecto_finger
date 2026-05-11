from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    TextAreaField,
    SubmitField,
    SelectField,
    DateField
)

from wtforms.validators import Optional


class ActividadCognitivaForm(FlaskForm):

    # ==========================================
    # DATOS GENERALES
    # ==========================================

    fecha_evaluacion = DateField(
        "Fecha de evaluación",
        validators=[Optional()]
    )

    examinador = StringField(
        "Examinador",
        validators=[Optional()]
    )

    edad = IntegerField(
        "Edad",
        validators=[Optional()]
    )

    sexo = SelectField(
        "Sexo",
        choices=[
            (" masculino", "Masculino"),
            (" femenino", "Femenino")
        ],
        validators=[Optional()]
    )

    escolaridad_anios = IntegerField(
        "Años de escolaridad",
        validators=[Optional()]
    )

    idioma = SelectField(
        "Idioma",
        choices=[
            (" spanish", "Español"),
            (" english", "Inglés")
        ],
        validators=[Optional()]
    )

    ocupacion = StringField(
        "Ocupación",
        validators=[Optional()]
    )

    preferencia_manual = SelectField(
        "Preferencia manual",
        choices=[
            ("diestra", "Diestra"),
            ("zurda", "Zurda"),
            ("ambidiestro", "Ambidiestro")
        ],
        validators=[Optional()]
    )

    # ==========================================
    # MOCA
    # ==========================================

    moca_total = FloatField(
        "MOCA total",
        validators=[Optional()]
    )

    # ==========================================
    # DÍGITOS
    # ==========================================

    digitos_directos_total = FloatField(
        "Dígitos directos total",
        validators=[Optional()]
    )

    digitos_directos_longitud = FloatField(
        "Dígitos directos longitud",
        validators=[Optional()]
    )

    digitos_inversos_total = FloatField(
        "Dígitos inversos total",
        validators=[Optional()]
    )

    digitos_inversos_longitud = FloatField(
        "Dígitos inversos longitud",
        validators=[Optional()]
    )

    # ==========================================
    # TRAIL MAKING TEST
    # ==========================================

    trail_a_tiempo = FloatField(
        "Trail A tiempo",
        validators=[Optional()]
    )

    trail_a_lineas_tiempo = FloatField(
        "Trail A líneas/tiempo",
        validators=[Optional()]
    )

    trail_a_errores = IntegerField(
        "Trail A errores",
        validators=[Optional()]
    )

    trail_b_tiempo = FloatField(
        "Trail B tiempo",
        validators=[Optional()]
    )

    trail_b_lineas_tiempo = FloatField(
        "Trail B líneas/tiempo",
        validators=[Optional()]
    )

    trail_b_errores = IntegerField(
        "Trail B errores",
        validators=[Optional()]
    )

    # ==========================================
    # MINT-32
    # ==========================================

    mint_32_total = FloatField(
        "MINT-32",
        validators=[Optional()]
    )

    # ==========================================
    # FLUENCIA FONOLÓGICA
    # ==========================================

    fluencia_p = FloatField(
        "Fluencia letra P",
        validators=[Optional()]
    )

    fluencia_m = FloatField(
        "Fluencia letra M",
        validators=[Optional()]
    )

    # ==========================================
    # FLUIDEZ SEMÁNTICA
    # ==========================================

    fluidez_animales = FloatField(
        "Fluidez animales",
        validators=[Optional()]
    )

    fluidez_vegetales = FloatField(
        "Fluidez vegetales",
        validators=[Optional()]
    )

    # ==========================================
    # BENSON
    # ==========================================

    benson_copia_total = FloatField(
        "Benson copia",
        validators=[Optional()]
    )

    benson_recuerdo_total = FloatField(
        "Benson recuerdo",
        validators=[Optional()]
    )

    # ==========================================
    # CRAFT STORY
    # ==========================================

    craft_inmediato_textual = FloatField(
        "Craft inmediato textual",
        validators=[Optional()]
    )

    craft_inmediato_parafraseo = FloatField(
        "Craft inmediato parafraseo",
        validators=[Optional()]
    )

    craft_diferido_textual = FloatField(
        "Craft diferido textual",
        validators=[Optional()]
    )

    craft_diferido_parafraseo = FloatField(
        "Craft diferido parafraseo",
        validators=[Optional()]
    )

    # ==========================================
    # SUEÑO
    # ==========================================

    sueno_indice_calidad = FloatField(
        "Índice calidad de sueño",
        validators=[Optional()]
    )

    sueno_observaciones = TextAreaField(
        "Observaciones sueño",
        validators=[Optional()]
    )

    # ==========================================
    # BOTÓN
    # ==========================================

    submit = SubmitField("Guardar evaluación")