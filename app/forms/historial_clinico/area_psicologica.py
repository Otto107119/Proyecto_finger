from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional

class AreaPsicologicaForm(FlaskForm):
    episodios_positivos = TextAreaField("Episodios positivos de su vida", validators=[Optional()])

    estado_animo = SelectField(
        "Estado de ánimo generalmente",
        choices=[
            ("", "Seleccione"),
            ("Feliz", "Feliz"),
            ("Triste", "Triste"),
            ("Angustia", "Angustia"),
            ("Otro", "Otro")
        ],
        validators=[Optional()]
    )
    estado_animo_otro = StringField("Otro estado de ánimo", validators=[Optional()])

    perdidas = BooleanField("Pérdidas")
    perdidas_cuales = TextAreaField("¿Cuáles?", validators=[Optional()])

    duelo = BooleanField("Duelo")
    duelo_tiempo = StringField("Tiempo", validators=[Optional()])
    tipo_duelo = StringField("Tipo de duelo", validators=[Optional()])

    estres = BooleanField("Estrés")
    afronta_estres = TextAreaField("¿Cómo lo afronta?", validators=[Optional()])

    ejercita_memoria = BooleanField("Ejercita su memoria")
    ejercita_memoria_como = TextAreaField("¿Cómo?", validators=[Optional()])

    olvidos_frecuentes = BooleanField("Olvidos frecuentes")
    olvidos_cuales = TextAreaField("¿Cuáles?", validators=[Optional()])

    satisfecho_vida = BooleanField("Satisfecho en su vida")
    satisfecho_vida_por_que = TextAreaField("¿Por qué?", validators=[Optional()])

    influye_opinion_demas = BooleanField("Influye la opinión de los demás en usted")
    influye_opinion_por_que = TextAreaField("¿Por qué?", validators=[Optional()])

    episodios_negativos = TextAreaField("Episodios negativos de su vida", validators=[Optional()])

    orientacion_persona = StringField("Persona", validators=[Optional()])
    orientacion_espacio = StringField("Espacio", validators=[Optional()])
    orientacion_tiempo = StringField("Tiempo", validators=[Optional()])
    orientacion_orientador = StringField("Orientador(a)", validators=[Optional()])

    comunicacion_verbal = TextAreaField("Comunicación verbal", validators=[Optional()])
    comunicacion_no_verbal = TextAreaField("Comunicación no verbal", validators=[Optional()])

    submit = SubmitField("Guardar")