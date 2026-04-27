from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class EstudioComplementarioForm(FlaskForm):
    estudio = StringField("Estudio", validators=[Optional()])
    resultado = TextAreaField("Resultado", validators=[Optional()])
    tratamiento = TextAreaField("Tratamiento", validators=[Optional()])
    fecha_estudio = StringField("Fecha del estudio", validators=[Optional()])

    submit = SubmitField("Guardar")