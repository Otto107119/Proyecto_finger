from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistroForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    confirmar = PasswordField(
        "Confirmar Contraseña",
        validators=[DataRequired(), EqualTo("password")]
    )

    submit = SubmitField("Registrarse")


class LoginForm(FlaskForm):
    correo = StringField("Correo", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")