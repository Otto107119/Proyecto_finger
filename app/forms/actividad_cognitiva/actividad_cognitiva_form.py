from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    DateField,
    SelectField,
    SubmitField
)
from wtforms.validators import Optional, NumberRange


class ActividadCognitivaForm(FlaskForm):
    fecha_evaluacion = DateField("Fecha de evaluación", validators=[Optional()])
    examinador = StringField("Examinador", validators=[Optional()])

    escolaridad_anios = IntegerField("Años de escolaridad", validators=[Optional(), NumberRange(min=0, max=40)])
    ocupacion = StringField("Ocupación", validators=[Optional()])

    preferencia_manual = SelectField(
        "Preferencia manual",
        choices=[
            ("", "Seleccione"),
            ("Derecha", "Derecha"),
            ("Izquierda", "Izquierda"),
            ("Ambidiestro", "Ambidiestro")
        ],
        validators=[Optional()]
    )

    # Screening
    moca_total = IntegerField("MOCA total /30", validators=[Optional(), NumberRange(min=0, max=30)])

    # Atención
    digitos_directos_total = IntegerField("Dígitos orden directos /14", validators=[Optional(), NumberRange(min=0, max=14)])
    digitos_directos_longitud = IntegerField("Dígitos directos longitud /9", validators=[Optional(), NumberRange(min=0, max=9)])
    digitos_inversos_total = IntegerField("Dígitos orden inversos /8", validators=[Optional(), NumberRange(min=0, max=8)])
    digitos_inversos_longitud = IntegerField("Dígitos inversos longitud /8", validators=[Optional(), NumberRange(min=0, max=8)])

    # Trail A
    trail_a_tiempo = FloatField("Trail Making Test A - tiempo /150 seg", validators=[Optional(), NumberRange(min=0, max=150)])
    trail_a_errores = IntegerField("Trail Making Test A - errores", validators=[Optional(), NumberRange(min=0)])
    trail_a_lineas_correctas = IntegerField("Trail Making Test A - líneas correctas", validators=[Optional(), NumberRange(min=0)])

    # Trail B
    trail_b_tiempo = FloatField("Trail Making Test B - tiempo /300 seg", validators=[Optional(), NumberRange(min=0, max=300)])
    trail_b_errores = IntegerField("Trail Making Test B - errores", validators=[Optional(), NumberRange(min=0)])
    trail_b_lineas_correctas = IntegerField("Trail Making Test B - líneas correctas", validators=[Optional(), NumberRange(min=0)])

    # Lenguaje
    mint_32_total = IntegerField("MINT-32 /32", validators=[Optional(), NumberRange(min=0, max=32)])

    # Fluencia fonológica
    fluencia_p = IntegerField("Fluencia fonológica letra P /50", validators=[Optional(), NumberRange(min=0, max=50)])
    fluencia_m = IntegerField("Fluencia fonológica letra M /50", validators=[Optional(), NumberRange(min=0, max=50)])

    # Fluidez semántica
    animales_total = IntegerField("Fluidez semántica animales", validators=[Optional(), NumberRange(min=0)])
    vegetales_total = IntegerField("Fluidez semántica vegetales", validators=[Optional(), NumberRange(min=0)])

    # Benson
    benson_inmediata = FloatField("Benson inmediata /10", validators=[Optional(), NumberRange(min=0, max=10)])
    benson_diferida = FloatField("Benson diferida /10", validators=[Optional(), NumberRange(min=0, max=10)])

    # Craft Story
    craft_ri_44 = IntegerField("Craft Story R.I. /44", validators=[Optional(), NumberRange(min=0, max=44)])
    craft_ri_parafraseo_25 = IntegerField("Craft Story R.I. parafraseo /25", validators=[Optional(), NumberRange(min=0, max=25)])
    craft_rd_44 = IntegerField("Craft Story R.D. /44", validators=[Optional(), NumberRange(min=0, max=44)])
    craft_rd_parafraseo_25 = IntegerField("Craft Story R.D. parafraseo /25", validators=[Optional(), NumberRange(min=0, max=25)])

    submit = SubmitField("Guardar actividad cognitiva")