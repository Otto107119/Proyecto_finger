from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField


SI_NO_PUNTOS = [
    ("1", "Sí / Independiente (1 punto)"),
    ("0", "No / Dependiente (0 puntos)")
]


class ActividadSocialKatzForm(FlaskForm):
    bano = RadioField("1. Baño", choices=SI_NO_PUNTOS)
    vestido = RadioField("2. Vestido", choices=SI_NO_PUNTOS)
    uso_sanitario = RadioField("3. Uso del sanitario", choices=SI_NO_PUNTOS)
    transferencias = RadioField("4. Transferencias", choices=SI_NO_PUNTOS)
    continencia = RadioField("5. Continencia", choices=SI_NO_PUNTOS)
    alimentacion = RadioField("6. Alimentación", choices=SI_NO_PUNTOS)

    clasificacion_letra = SelectField(
        "Clasificación alfabética",
        choices=[
            ("", "Selecciona una opción"),
            ("A", "A - Independencia en todas las actividades"),
            ("B", "B - Independencia en todas excepto una"),
            ("C", "C - Independencia excepto bañarse y otra actividad"),
            ("D", "D - Independencia excepto bañarse, vestirse y otra actividad"),
            ("E", "E - Independencia excepto baño, vestido, sanitario y otra actividad"),
            ("F", "F - Independencia excepto baño, vestido, sanitario, transferencias y otra actividad"),
            ("G", "G - Dependencia en las seis actividades"),
            ("H", "H - Dependencia en dos actividades pero no clasifica en C, D, E y F"),
        ]
    )