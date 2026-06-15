from flask_wtf import FlaskForm
from wtforms import RadioField


SI_NO = [
    ("si", "Sí"),
    ("no", "No")
]


class ActividadSocialGDS15Form(FlaskForm):
    p1 = RadioField("1. ¿En general, está satisfecho(a) con su vida?", choices=SI_NO)
    p2 = RadioField("2. ¿Ha abandonado muchas de sus tareas habituales y aficiones?", choices=SI_NO)
    p3 = RadioField("3. ¿Siente que su vida está vacía?", choices=SI_NO)
    p4 = RadioField("4. ¿Se siente con frecuencia aburrido(a)?", choices=SI_NO)
    p5 = RadioField("5. ¿Se encuentra de buen humor la mayor parte del tiempo?", choices=SI_NO)
    p6 = RadioField("6. ¿Teme que algo malo pueda ocurrirle?", choices=SI_NO)
    p7 = RadioField("7. ¿Se siente feliz la mayor parte del tiempo?", choices=SI_NO)
    p8 = RadioField("8. ¿Con frecuencia se siente desamparado(a), desprotegido(a)?", choices=SI_NO)
    p9 = RadioField("9. ¿Prefiere quedarse en casa, más que salir y hacer cosas nuevas?", choices=SI_NO)
    p10 = RadioField("10. ¿Cree que tiene más problemas de memoria que la mayoría de la gente?", choices=SI_NO)
    p11 = RadioField("11. ¿En estos momentos, piensa que es estupendo estar vivo(a)?", choices=SI_NO)
    p12 = RadioField("12. ¿Actualmente se siente un(a) inútil?", choices=SI_NO)
    p13 = RadioField("13. ¿Se siente lleno(a) de energía?", choices=SI_NO)
    p14 = RadioField("14. ¿Se siente sin esperanza en este momento?", choices=SI_NO)
    p15 = RadioField("15. ¿Piensa que la mayoría de la gente está en mejor situación que usted?", choices=SI_NO)