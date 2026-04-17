from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField, DecimalField, SubmitField
from wtforms.validators import Optional


class ActividadSocialForm(FlaskForm):
    seguridad_social = StringField("Seguridad social", validators=[Optional()])
    tiempo_residencia_ameca = IntegerField("Tiempo de residencia en Ameca", validators=[Optional()])
    tipo_vivienda = StringField("Tipo de vivienda", validators=[Optional()])
    migracion = BooleanField("Migración")
    observaciones = TextAreaField("Observaciones", validators=[Optional()])

    ingreso_entrevistado = DecimalField("Ingreso entrevistado", validators=[Optional()], places=2)
    otros_ingresos = DecimalField("Otros ingresos", validators=[Optional()], places=2)

    renta = DecimalField("Renta", validators=[Optional()], places=2)
    colegiaturas = DecimalField("Colegiaturas", validators=[Optional()], places=2)
    alimentacion = DecimalField("Alimentación", validators=[Optional()], places=2)
    gastos_medicos = DecimalField("Gastos médicos", validators=[Optional()], places=2)
    transporte = DecimalField("Transporte", validators=[Optional()], places=2)
    diversion = DecimalField("Diversión", validators=[Optional()], places=2)
    gasolina = DecimalField("Gasolina", validators=[Optional()], places=2)
    pagos_tarjetas = DecimalField("Pagos tarjetas", validators=[Optional()], places=2)
    luz = DecimalField("Luz", validators=[Optional()], places=2)
    ahorro = DecimalField("Ahorro", validators=[Optional()], places=2)
    agua = DecimalField("Agua", validators=[Optional()], places=2)
    deudas = DecimalField("Deudas", validators=[Optional()], places=2)
    gas = DecimalField("Gas", validators=[Optional()], places=2)
    ropa = DecimalField("Ropa", validators=[Optional()], places=2)
    telefono = DecimalField("Teléfono", validators=[Optional()], places=2)
    calzado = DecimalField("Calzado", validators=[Optional()], places=2)
    telefono_celular = DecimalField("Teléfono celular", validators=[Optional()], places=2)
    alcohol_cigarros = DecimalField("Alcohol / cigarros", validators=[Optional()], places=2)
    cable = DecimalField("Cable", validators=[Optional()], places=2)
    internet = DecimalField("Internet", validators=[Optional()], places=2)
    otros_gastos = DecimalField("Otros gastos", validators=[Optional()], places=2)
    empleados_domesticos = DecimalField("Empleados domésticos", validators=[Optional()], places=2)

    padre_nombre = StringField("Nombre del padre", validators=[Optional()])
    padre_edad_o_tiempo_vida = IntegerField("Edad o tiempo de vida del padre", validators=[Optional()])
    padre_vive = BooleanField("El padre vive")
    padre_causa_muerte = StringField("Causa de muerte del padre", validators=[Optional()])
    padre_enfermedad = StringField("Enfermedad del padre", validators=[Optional()])

    madre_nombre = StringField("Nombre de la madre", validators=[Optional()])
    madre_edad_o_tiempo_vida = IntegerField("Edad o tiempo de vida de la madre", validators=[Optional()])
    madre_vive = BooleanField("La madre vive")
    madre_causa_muerte = StringField("Causa de muerte de la madre", validators=[Optional()])
    madre_enfermedad = StringField("Enfermedad de la madre", validators=[Optional()])

    submit = SubmitField("Guardar actividad social")


class HermanoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    edad = IntegerField("Edad", validators=[Optional()])
    relacion = StringField("Relación", validators=[Optional()])
    donde_vive = StringField("Dónde vive", validators=[Optional()])
    enfermedad = StringField("Enfermedad", validators=[Optional()])
    submit = SubmitField("Agregar hermano")


class HijoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    edad = IntegerField("Edad", validators=[Optional()])
    estado_civil = StringField("Estado civil", validators=[Optional()])
    relacion = StringField("Relación", validators=[Optional()])
    donde_vive = StringField("Dónde vive", validators=[Optional()])
    enfermedad = StringField("Enfermedad", validators=[Optional()])
    numero_hijos = IntegerField("Número de hijos", validators=[Optional()])
    submit = SubmitField("Agregar hijo")