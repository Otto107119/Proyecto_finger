from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import Optional, NumberRange


OPCIONES_LAWTON_KATZ = [
    ("", "Seleccionar"),
    ("I", "I - Independiente"),
    ("A", "A - Con asistencia"),
    ("D", "D - Dependiente"),
]


class ActividadSocialSaludMentalForm(FlaskForm):
    # GDS 15
    gds_total = IntegerField(
        "GDS total",
        validators=[Optional(), NumberRange(min=0, max=15)]
    )

    # Lawton y Brody
    lawton_telefono = SelectField("Teléfono", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_transporte = SelectField("Transporte", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_compras = SelectField("Compras", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_alimentos = SelectField("Preparación de alimentos", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_hogar = SelectField("Quehaceres del hogar", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_medicacion = SelectField("Medicación", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    lawton_dinero = SelectField("Manejo del dinero", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])

    # Katz
    katz_banio = SelectField("Baño", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    katz_vestido = SelectField("Vestido", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    katz_sanitario = SelectField("Uso de sanitario", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    katz_transferencia = SelectField("Transferencia", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    katz_continencia = SelectField("Continencia", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])
    katz_alimentacion = SelectField("Alimentación", choices=OPCIONES_LAWTON_KATZ, validators=[Optional()])

    katz_letra = SelectField(
        "Clasificación alfabética Katz",
        choices=[
            ("", "Seleccionar"),
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
            ("F", "F"),
            ("G", "G"),
            ("Otro", "Otro"),
        ],
        validators=[Optional()]
    )

    submit = SubmitField("Guardar salud mental")