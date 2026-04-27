from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class APPResumenForm(FlaskForm):
    numero_embarazos = StringField("Número de embarazos", validators=[Optional()])
    farmacos_no_especificados = TextAreaField("Fármacos no especificados", validators=[Optional()])
    medicina_alterna = TextAreaField("Medicina alterna", validators=[Optional()])

    submit = SubmitField("Guardar")


class APPPatologiaForm(FlaskForm):
    patologia = StringField("Patología", validators=[Optional()])
    hace_cuanto = StringField("Hace cuánto", validators=[Optional()])
    diagnostico = StringField("Diagnóstico", validators=[Optional()])
    farmaco = StringField("Fármaco", validators=[Optional()])
    dosis = StringField("Dosis", validators=[Optional()])

    submit = SubmitField("Guardar")