from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional

class AreaSocialForm(FlaskForm):
    tiene_hijos = BooleanField("Tiene hijos")
    hijas_mujeres = IntegerField("Mujeres", validators=[Optional()])
    hijos_hombres = IntegerField("Hombres", validators=[Optional()])
    vive_con = StringField("Vive con", validators=[Optional()])
    pension = BooleanField("Pensión")
    pension_cual = StringField("¿Cuál?", validators=[Optional()])
    ingreso_familiar_mensual = StringField("Monto de ingreso familiar al mes", validators=[Optional()])

    red_apoyo_amigos = BooleanField("Amigos")
    red_apoyo_familia = BooleanField("Familia")
    red_apoyo_vecinos = BooleanField("Vecinos")
    red_apoyo_nietos = BooleanField("Nietos")

    costumbres_tradiciones = TextAreaField("Costumbres y tradiciones", validators=[Optional()])
    actividades_gusta = TextAreaField("Actividades que le gusta realizar", validators=[Optional()])
    actividades_anteriores = TextAreaField("Actividades anteriores", validators=[Optional()])
    actividades_actuales = TextAreaField("Actividades actuales", validators=[Optional()])

    acude_taller = BooleanField("Acude a algún taller")
    taller_cual = StringField("¿Cuál taller?", validators=[Optional()])

    frecuencia_sale_semana = StringField("Frecuencia con la que sale de su casa por semana", validators=[Optional()])
    con_quien_sale = StringField("¿Con quién sale?", validators=[Optional()])

    cuidador = BooleanField("Cuidador")
    cuidador_quien = StringField("¿Quién?", validators=[Optional()])
    cuidador_remunerado = BooleanField("Remunerado")
    cuidador_antiguedad = StringField("Antigüedad", validators=[Optional()])
    cuidador_nombre = StringField("Nombre del cuidador", validators=[Optional()])
    cuidador_telefono = StringField("Teléfono del cuidador", validators=[Optional()])

    decide_asuntos_familiares = BooleanField("Decide asuntos familiares")
    relacion_familia = SelectField(
        "Relación con la familia",
        choices=[("", "Seleccione"), ("Buena", "Buena"), ("Mala", "Mala")],
        validators=[Optional()]
    )
    problemas_familiares = BooleanField("Problemas")
    tipo_problemas_familiares = StringField("Tipo de problema", validators=[Optional()])

    riesgos_entorno_social = TextAreaField("Riesgos en su entorno social", validators=[Optional()])
    medio_transporte_habitual = StringField("Medio de transporte habitual", validators=[Optional()])
    pasa_dia_con = StringField("Pasa el día con", validators=[Optional()])

    submit = SubmitField("Guardar")