from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Optional


class HermanoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    edad = IntegerField("Edad", validators=[Optional()])
    relacion = StringField("Relación", validators=[Optional()])
    donde_vive = StringField("Dónde vive", validators=[Optional()])
    enfermedad = StringField("Enfermedad", validators=[Optional()])
    submit = SubmitField("Agregar hermano")