from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired


class PacienteForm(FlaskForm):
    nombre = StringField("Nombre completo", validators=[DataRequired()])

    fecha_nacimiento = DateField(
        "Fecha de nacimiento",
        format="%Y-%m-%d",
        validators=[DataRequired()]
    )

    genero = SelectField(
        "Género",
        choices=[
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro")
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Guardar paciente")