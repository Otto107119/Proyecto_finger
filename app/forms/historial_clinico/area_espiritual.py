from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional

class AreaEspiritualForm(FlaskForm):
    sentido_vida = TextAreaField("Sentido de vida (¿Qué te motiva?)", validators=[Optional()])
    mision_vida = TextAreaField("Misión de su vida", validators=[Optional()])
    miedo_morir = BooleanField("Miedo a morir")
    piensa_muerte = TextAreaField("¿Qué piensa sobre la muerte?", validators=[Optional()])
    principales_miedos = TextAreaField("Principales miedos", validators=[Optional()])
    metas_vida = TextAreaField("Metas en su vida (¿Qué más quiere hacer?)", validators=[Optional()])

    submit = SubmitField("Guardar")