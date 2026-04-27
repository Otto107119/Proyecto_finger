from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class MarchaEquilibrioForm(FlaskForm):
    cifosis = BooleanField("Cifosis")
    lordosis = BooleanField("Lordosis")
    escoliosis = BooleanField("Escoliosis")

    mareos = BooleanField("Mareos")
    sincope = BooleanField("Síncope")

    caidas = BooleanField("Caídas")
    frecuencia_caidas = StringField("Frecuencia de caídas", validators=[Optional()])

    fracturas = BooleanField("Fracturas")
    antiguedad_fracturas = StringField("Antigüedad de fracturas", validators=[Optional()])

    consecuencias_secuelas = TextAreaField("Consecuencias / secuelas", validators=[Optional()])
    ayudas_tecnicas = TextAreaField("Ayudas técnicas", validators=[Optional()])

    submit = SubmitField("Guardar")