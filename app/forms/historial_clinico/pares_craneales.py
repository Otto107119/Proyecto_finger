from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional

ESTADO_PAR_CHOICES = [
    ("", "Seleccione"),
    ("Normal", "Normal"),
    ("Alterado", "Alterado"),
    ("No valorado", "No valorado"),
]

CONSISTENCIA_CHOICES = [
    ("", "Seleccione"),
    ("Molido", "Molido"),
    ("Entero", "Entero"),
]

class ParesCranealesForm(FlaskForm):
    pc_i_estado = SelectField("I. Olfatorio", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_i_observacion = TextAreaField("Observación I", validators=[Optional()])

    pc_ii_estado = SelectField("II. Óptico", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_ii_observacion = TextAreaField("Observación II", validators=[Optional()])

    pc_iii_estado = SelectField("III. Motor ocular común", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_iii_observacion = TextAreaField("Observación III", validators=[Optional()])

    pc_iv_estado = SelectField("IV. Troclear", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_iv_observacion = TextAreaField("Observación IV", validators=[Optional()])

    pc_v_estado = SelectField("V. Trigémino", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_v_observacion = TextAreaField("Observación V", validators=[Optional()])

    pc_vi_estado = SelectField("VI. Abducens", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_vi_observacion = TextAreaField("Observación VI", validators=[Optional()])

    pc_vii_estado = SelectField("VII. Facial", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_vii_observacion = TextAreaField("Observación VII", validators=[Optional()])

    pc_viii_estado = SelectField("VIII. Vestibulococlear", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_viii_observacion = TextAreaField("Observación VIII", validators=[Optional()])

    pc_ix_estado = SelectField("IX. Glosofaríngeo", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_ix_observacion = TextAreaField("Observación IX", validators=[Optional()])

    pc_x_estado = SelectField("X. Vago", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_x_observacion = TextAreaField("Observación X", validators=[Optional()])

    pc_xi_estado = SelectField("XI. Accesorio", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_xi_observacion = TextAreaField("Observación XI", validators=[Optional()])

    pc_xii_estado = SelectField("XII. Hipogloso", choices=ESTADO_PAR_CHOICES, validators=[Optional()])
    pc_xii_observacion = TextAreaField("Observación XII", validators=[Optional()])

    observaciones_generales = TextAreaField("Observaciones generales", validators=[Optional()])

    dentadura_postiza = BooleanField("Dentadura postiza")
    removible = BooleanField("Removible")
    piezas_perdidas = TextAreaField("Piezas perdidas", validators=[Optional()])
    piezas_conservadas = TextAreaField("Piezas conservadas", validators=[Optional()])
    piezas_fragiles = TextAreaField("Piezas frágiles", validators=[Optional()])
    problemas_masticar = BooleanField("Problemas al masticar")
    consistencia_alimentos = SelectField("Consistencia de alimentos", choices=CONSISTENCIA_CHOICES, validators=[Optional()])
    atragantamientos = BooleanField("Atragantamientos")

    submit = SubmitField("Guardar")