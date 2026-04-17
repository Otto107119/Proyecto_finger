from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ActividadFisicaForm(FlaskForm):
    tipo = StringField("Tipo de actividad", validators=[DataRequired()])
    duracion_min = IntegerField(
        "Duración (minutos)",
        validators=[DataRequired(), NumberRange(min=1, max=600)]
    )
    observaciones = TextAreaField("Observaciones (opcional)")
    submit = SubmitField("Guardar actividad")