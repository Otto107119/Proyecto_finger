from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, FloatField, BooleanField, SubmitField
from wtforms.validators import Optional, NumberRange


class AreaMedicaForm(FlaskForm):


    presion_sistolica = FloatField(
        "Presión sanguínea sistólica (mmHg)",
        validators=[Optional()]
    )

    tratamiento_hipertension = BooleanField("Tratamiento por hipertensión")
    fumador = BooleanField("Fumador")
    diabetico = BooleanField("Diabético")

    hdl = FloatField("HDL", validators=[Optional()])
    colesterol = FloatField("Colesterol", validators=[Optional()])

    edad_corazon = FloatField("Edad del corazón", validators=[Optional()])
    porcentaje_riesgo = FloatField("Porcentaje de riesgo", validators=[Optional()])

    colesterol_total = FloatField("Colesterol total", validators=[Optional()])
    colesterol_ldl = FloatField("Colesterol LDL", validators=[Optional()])
    colesterol_hdl = FloatField("Colesterol HDL", validators=[Optional()])
    trigliceridos = FloatField("Triglicéridos", validators=[Optional()])

    glucosa_capilar = FloatField("Glucosa capilar", validators=[Optional()])

    submit = SubmitField("Guardar área médica")