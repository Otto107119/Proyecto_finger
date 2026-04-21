from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, DateField, SubmitField
from wtforms.validators import Optional

class DatosGeneralesForm(FlaskForm):
    fecha = DateField("Fecha", format="%Y-%m-%d", validators=[Optional()])

    contacto_nombre = StringField("Nombre contacto 1", validators=[Optional()])
    contacto_telefono = StringField("Teléfono contacto 1", validators=[Optional()])
    contacto_nombre_2 = StringField("Nombre contacto 2", validators=[Optional()])
    contacto_telefono_2 = StringField("Teléfono contacto 2", validators=[Optional()])

    fuente_valoracion = SelectField(
        "Fuente de valoración",
        choices=[
            ("", "Seleccione"),
            ("Usuario", "Usuario"),
            ("Familiar", "Familiar"),
            ("Cuidador principal", "Cuidador principal")
        ],
        validators=[Optional()]
    )

    escolaridad = StringField("Escolaridad", validators=[Optional()])
    sabe_leer = BooleanField("Sabe leer")
    sabe_escribir = BooleanField("Sabe escribir")
    estado_civil = StringField("Estado civil", validators=[Optional()])
    ocupacion_anterior = StringField("Ocupación anterior", validators=[Optional()])
    ocupacion_actual = StringField("Ocupación actual", validators=[Optional()])
    domicilio_origen = TextAreaField("Domicilio de origen", validators=[Optional()])
    domicilio_actual = TextAreaField("Domicilio actual", validators=[Optional()])

    nucleo_procedencia = SelectField(
        "Núcleo de procedencia",
        choices=[("", "Seleccione"), ("Rural", "Rural"), ("Urbano", "Urbano")],
        validators=[Optional()]
    )

    vivienda = SelectField(
        "Vivienda",
        choices=[("", "Seleccione"), ("Propia", "Propia"), ("Rentada", "Rentada"), ("Prestada", "Prestada")],
        validators=[Optional()]
    )

    servicio_luz = BooleanField("Luz")
    servicio_agua = BooleanField("Agua")
    servicio_tel = BooleanField("Teléfono")
    servicio_internet = BooleanField("Internet")

    motivo_consulta = TextAreaField("Motivo de consulta", validators=[Optional()])

    submit = SubmitField("Guardar")