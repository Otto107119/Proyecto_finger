from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional


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


class HistorialClinicoForm(FlaskForm):
    # DATOS GENERALES
    fecha_formulario = DateField("Fecha", validators=[Optional()])
    fecha_nacimiento = DateField("Fecha de nacimiento", validators=[Optional()])
    estado_civil = SelectField(
        "Estado civil",
        choices=[
            ("", "Seleccione"),
            ("soltero", "Soltero(a)"),
            ("casado", "Casado(a)"),
            ("union_libre", "Unión libre"),
            ("viudo", "Viudo(a)"),
            ("divorciado", "Divorciado(a)")
        ],
        validators=[Optional()]
    )
    numero_contacto = StringField("Número de contacto", validators=[Optional()])
    domicilio = StringField("Domicilio", validators=[Optional()])
    grado_escolaridad = SelectField(
        "Grado de escolaridad",
        choices=[
            ("", "Seleccione"),
            ("sin_escolaridad", "Sin escolaridad"),
            ("primaria", "Primaria"),
            ("secundaria", "Secundaria"),
            ("preparatoria", "Preparatoria"),
            ("tecnica", "Carrera técnica"),
            ("licenciatura", "Licenciatura"),
            ("posgrado", "Posgrado")
        ],
        validators=[Optional()]
    )
    familiar_confianza_nombre = StringField("Nombre del familiar de confianza", validators=[Optional()])
    familiar_confianza_telefono = StringField("Teléfono del familiar de confianza", validators=[Optional()])
    expectativas_participacion = TextAreaField("Expectativas de participación", validators=[Optional()])

    # ANTECEDENTES
    padece_enfermedad_actual = BooleanField("¿Padece alguna enfermedad actual?")
    enfermedad_actual_detalle = TextAreaField("Detalle de enfermedad actual", validators=[Optional()])

    consume_medicamentos = BooleanField("¿Consume medicamentos?")
    medicamentos_detalle = TextAreaField("Detalle de medicamentos", validators=[Optional()])

    cirugias_previas = BooleanField("¿Ha tenido cirugías previas?")
    cirugias_detalle = TextAreaField("Detalle de cirugías", validators=[Optional()])

    problemas_vision = BooleanField("¿Presenta problemas de visión?")
    problemas_audicion = BooleanField("¿Presenta problemas de audición?")

    impedimento_actividad_fisica = BooleanField("¿Tiene impedimento para actividad física?")
    impedimento_detalle = TextAreaField("Detalle del impedimento", validators=[Optional()])

    usa_dispositivo_apoyo = BooleanField("¿Usa dispositivo de apoyo?")
    dispositivo_apoyo_detalle = TextAreaField("Detalle del dispositivo de apoyo", validators=[Optional()])

    # SOCIODEMOGRÁFICO
    situacion_laboral_actual = SelectField(
        "Situación laboral actual",
        choices=[
            ("", "Seleccione"),
            ("empleado", "Empleado"),
            ("desempleado", "Desempleado"),
            ("jubilado", "Jubilado"),
            ("hogar", "Hogar"),
            ("otro", "Otro")
        ],
        validators=[Optional()]
    )
    ocupacion_profesion_anterior = StringField("Ocupación o profesión anterior", validators=[Optional()])
    fuente_principal_ingresos = StringField("Fuente principal de ingresos", validators=[Optional()])
    situacion_economica_actual = SelectField(
        "Situación económica actual",
        choices=[
            ("", "Seleccione"),
            ("buena", "Buena"),
            ("regular", "Regular"),
            ("mala", "Mala")
        ],
        validators=[Optional()]
    )
    cuenta_seguro_salud = BooleanField("¿Cuenta con seguro de salud?")
    recibe_ayuda_economica = BooleanField("¿Recibe ayuda económica?")
    tipo_vivienda = SelectField(
        "Tipo de vivienda",
        choices=[
            ("", "Seleccione"),
            ("casa", "Casa"),
            ("departamento", "Departamento"),
            ("otro", "Otro")
        ],
        validators=[Optional()]
    )
    condicion_vivienda = SelectField(
        "Condición de vivienda",
        choices=[
            ("", "Seleccione"),
            ("propia", "Propia"),
            ("rentada", "Rentada"),
            ("prestada", "Prestada"),
            ("otro", "Otro")
        ],
        validators=[Optional()]
    )
    personas_hogar = IntegerField("Número de personas en el hogar", validators=[Optional()])
    rol_hogar = StringField("Rol dentro del hogar", validators=[Optional()])
    participa_actividades_sociales = BooleanField("¿Participa en actividades sociales?")
    frecuencia_actividad_fisica = SelectField(
        "Frecuencia de actividad física",
        choices=[
            ("", "Seleccione"),
            ("nunca", "Nunca"),
            ("1_2_semana", "1 a 2 veces por semana"),
            ("3_4_semana", "3 a 4 veces por semana"),
            ("diario", "Diario")
        ],
        validators=[Optional()]
    )
    situacion_sociodemografica_adicional = TextAreaField("Situación sociodemográfica adicional", validators=[Optional()])

    # OBSERVACIONES
    observaciones_entrevista = TextAreaField("Observaciones de la entrevista", validators=[Optional()])

    submit = SubmitField("Guardar historial clínico")

