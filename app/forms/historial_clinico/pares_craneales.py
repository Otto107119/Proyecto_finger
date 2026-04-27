from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, SelectField, SubmitField
from wtforms.validators import Optional

CONSISTENCIA_CHOICES = [
    ("", "Seleccione"),
    ("Molido", "Molido"),
    ("Entero", "Entero"),
]

class ParesCranealesForm(FlaskForm):
    evaluados = BooleanField("Pares craneales evaluados")
    sin_alteraciones = BooleanField("Sin alteraciones")
    alteraciones = TextAreaField("Alteraciones encontradas", validators=[Optional()])
    observaciones_generales = TextAreaField("Observaciones generales", validators=[Optional()])

    dentadura_postiza = BooleanField("Dentadura postiza")
    removible = BooleanField("Removible")
    piezas_perdidas = TextAreaField("Piezas perdidas", validators=[Optional()])
    piezas_conservadas = TextAreaField("Piezas conservadas", validators=[Optional()])
    piezas_fragiles = TextAreaField("Piezas frágiles", validators=[Optional()])
    problemas_masticar = BooleanField("Problemas al masticar")
    consistencia_alimentos = SelectField(
        "Consistencia de alimentos",
        choices=CONSISTENCIA_CHOICES,
        validators=[Optional()]
    )
    atragantamientos = BooleanField("Atragantamientos")

    submit = SubmitField("Guardar")