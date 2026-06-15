from flask_wtf import FlaskForm
from wtforms import RadioField


LAWTON_OPCIONES = [
    ("3", "Independiente (3 puntos)"),
    ("2", "Con asistencia (2 puntos)"),
    ("1", "Dependiente (1 punto)")
]


class ActividadSocialLawtonBrodyForm(FlaskForm):
    telefono = RadioField("1. Teléfono", choices=LAWTON_OPCIONES)
    transporte = RadioField("2. Transporte", choices=LAWTON_OPCIONES)
    compras = RadioField("3. Compras", choices=LAWTON_OPCIONES)
    preparacion_alimentos = RadioField("4. Preparación de alimentos", choices=LAWTON_OPCIONES)
    quehaceres_hogar = RadioField("5. Quehaceres del hogar", choices=LAWTON_OPCIONES)
    medicacion = RadioField("6. Medicación", choices=LAWTON_OPCIONES)
    manejo_dinero = RadioField("7. Manejo de dinero", choices=LAWTON_OPCIONES)