from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    confirmar = PasswordField("Confirmar Contraseña",
                              validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")
    
class PacienteForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired()])
    edad = IntegerField("Edad", validators=[DataRequired(), NumberRange(min=0, max=130)])
    genero = SelectField("Género", choices=[
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro")
    ], validators=[DataRequired()])

    submit = SubmitField("Guardar paciente")

class ActividadFisicaForm(FlaskForm):
    tipo = StringField("Tipo de actividad", validators=[DataRequired()])
    duracion_min = IntegerField("Duración (minutos)", validators=[DataRequired(), NumberRange(min=1, max=600)])
    observaciones = TextAreaField("Observaciones (opcional)")
    submit = SubmitField("Guardar actividad")

