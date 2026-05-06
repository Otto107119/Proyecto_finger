from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import Optional, NumberRange


class ActividadFisicaForm(FlaskForm):
    sentarse_levantarse_30s = IntegerField(
        "Test sentarse y levantarse 30 segundos",
        validators=[Optional(), NumberRange(min=0)]
    )

    dinamometro_kg = FloatField(
        "Presión manual / Dinamómetro (kg)",
        validators=[Optional(), NumberRange(min=0)]
    )

    tug_segundos = FloatField(
        "Time Up and Go - TUG (segundos)",
        validators=[Optional(), NumberRange(min=0)]
    )

    equilibrio_unipodal_segundos = FloatField(
        "Equilibrio unipodal (segundos)",
        validators=[Optional(), NumberRange(min=0)]
    )

    caminata_6min_metros = FloatField(
        "Caminata 6 minutos (metros)",
        validators=[Optional(), NumberRange(min=0)]
    )

    velocidad_marcha_ms = FloatField(
        "Velocidad de marcha (m/s)",
        validators=[Optional(), NumberRange(min=0)]
    )

    sppb_equilibrio = IntegerField(
        "SPPB - Equilibrio (0 a 4)",
        validators=[Optional(), NumberRange(min=0, max=4)]
    )

    sppb_velocidad_marcha = IntegerField(
        "SPPB - Velocidad de marcha (0 a 4)",
        validators=[Optional(), NumberRange(min=0, max=4)]
    )

    sppb_fuerza_piernas = IntegerField(
        "SPPB - Fuerza de piernas (0 a 4)",
        validators=[Optional(), NumberRange(min=0, max=4)]
    )

    notas = TextAreaField("Notas clínicas", validators=[Optional()])

    submit = SubmitField("Guardar evaluación")