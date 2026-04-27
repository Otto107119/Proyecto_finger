from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class FactoresRiesgoForm(FlaskForm):
    alcohol = BooleanField("Alcohol")
    frecuencia_alcohol = StringField("Frecuencia de alcohol", validators=[Optional()])

    tabaco = BooleanField("Tabaco")
    frecuencia_tabaco = StringField("Frecuencia de tabaco", validators=[Optional()])

    drogas = BooleanField("Drogas")
    frecuencia_drogas = StringField("Frecuencia de drogas", validators=[Optional()])

    vida_sexual_activa = BooleanField("Vida sexual activa")
    frecuencia_vida_sexual = StringField("Frecuencia de vida sexual", validators=[Optional()])

    observaciones = TextAreaField("Observaciones", validators=[Optional()])

    submit = SubmitField("Guardar")