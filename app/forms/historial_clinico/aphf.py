from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class APHFForm(FlaskForm):
    vive_padre = BooleanField("Padre vive")
    edad_padre = StringField("Edad del padre", validators=[Optional()])
    padecimientos_padre = TextAreaField("Padecimientos del padre", validators=[Optional()])

    vive_madre = BooleanField("Madre vive")
    edad_madre = StringField("Edad de la madre", validators=[Optional()])
    padecimientos_madre = TextAreaField("Padecimientos de la madre", validators=[Optional()])

    numero_hermanos = StringField("Número de hermanos", validators=[Optional()])
    padecimientos_hermanos = TextAreaField("Padecimientos de hermanos", validators=[Optional()])

    numero_hijos = StringField("Número de hijos", validators=[Optional()])
    padecimientos_hijos = TextAreaField("Padecimientos de hijos", validators=[Optional()])

    diabetes = BooleanField("Diabetes")
    hipertension = BooleanField("Hipertensión")
    cancer = BooleanField("Cáncer")
    cardiopatias = BooleanField("Cardiopatías")
    obesidad = BooleanField("Obesidad")
    demencia = BooleanField("Demencia")
    alzheimer = BooleanField("Alzheimer")
    parkinson = BooleanField("Parkinson")
    enfermedad_renal = BooleanField("Enfermedad renal")

    otra_enfermedad = StringField("Otra enfermedad", validators=[Optional()])
    observaciones = TextAreaField("Observaciones", validators=[Optional()])

    submit = SubmitField("Guardar")