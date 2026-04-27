from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Optional


class VisitaEspecialistaForm(FlaskForm):
    fecha_visita = StringField("Fecha de visita", validators=[Optional()])
    especialista = StringField("Especialista", validators=[Optional()])
    motivo = TextAreaField("Motivo", validators=[Optional()])
    tratamiento = TextAreaField("Tratamiento", validators=[Optional()])
    estudios_requeridos = TextAreaField("Estudios que se requieren", validators=[Optional()])

    submit = SubmitField("Guardar")