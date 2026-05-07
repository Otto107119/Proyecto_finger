from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

usuarios = [
    ("Bolaños Miranda Iriarte", "iriarte.bolanos@valles.udg.mx", "cuvalles26", "admin", "actividad_fisica"),
    ("Figueroa Jiménez María Dolores", "maria.figueroa@academicos.udg.mx", "cuvalles26", "admin", "actividad_cognitiva"),
    ("Guzmán Arrañaga Karla Cristina", "karla.guzman@academicos.udg.mx", "cuvalles26", "superadmin", "todas"),
    ("Hernández Magaña Carmen Elvira", "carmen.hernandez@valles.udg.mx", "cuvalles26", "admin", "actividad_social"),
    ("Morales Núñez José Javier", "javier.morales@academicos.udg.mx", "cuvalles26", "admin", "area_medica"),
    ("Rentería Vargas Erasmo Misael", "erasmo.renteria@academicos.udg.mx", "cuvalles26", "superadmin", "todas"),
    ("Vázquez Aguilar Laura Alejandra", "alejandra.vazquez@academicos.udg.mx", "cuvalles26", "admin", "actividad_nutricional"),
    ("Velázquez Sevilla Shayra Inocencia", "shayra.velazquez@academicos.udg.mx", "cuvalles26", "admin", "actividad_social"),

    ("Ávila Nungaray María del Rosario", "maria.avila8099@alumnos.udg.mx", "cuvalles26", "capturista", "historial_clinico"),
    ("Fernández Espada Darelis", "darelisfernandezespada@gmail.com", "cuvalles26", "capturista", "actividad_cognitiva,area_medica"),
    ("González Pérez Cinthya Yazmín", "cinthya.gonzalez7151@alumnos.udg.mx", "cuvalles26", "capturista", "actividad_nutricional"),
    ("Miranda Castillo Melissa Bárbara", "melissabarbaramirandacastillo@gmail.com", "cuvalles26", "capturista", "actividad_cognitiva,area_medica"),
    ("Montelongo Zárate María de Jesús", "maria.montelongo5870@alumnos.udg.mx", "cuvalles26", "capturista", "actividad_fisica"),
    ("Pacheco Valdivia Ivana Betzabé", "ivana.pacheco7172@alumnos.udg.mx", "cuvalles26", "capturista", "historial_clinico"),
    ("Ruiz Esquivel Esmeralda", "esmeralda.ruiz3532@alumnos.udg.mx", "cuvalles26", "capturista", "area_medica"),
    ("Estrada Montes Valeria Jaqueline", "valeria.estrada9555@alumnos.udg.mx", "cuvalles26", "capturista", "actividad_cognitiva"),
    ("Fausto Rubio Cecilia Guadalupe", "cgfausto9@gmail.com", "cuvalles26", "capturista", "actividad_cognitiva"),
    ("Ramírez Hernández Ernesto Imanol", "ernesto.ramirez7075@alumnos.udg.mx", "cuvalles26", "superadmin", "todas"),
    ("Santillán Díaz Andrómeda Guicela", "andromeda.santillan0696@alumnos.udg.mx", "cuvalles26", "capturista", "actividad_fisica,actividad_cognitiva"),
    ("Sosa Peña Diego", "sosa.dp04@gmail.com", "cuvalles26", "capturista", "actividad_cognitiva"),
]


with app.app_context():
    Usuario.query.delete()
    db.session.commit()

    for nombre, email, password, rol, area in usuarios:
        usuario = Usuario(
            nombre=nombre,
            correo=email,
            rol=rol,
            area=area,
        )

        usuario.set_password(password)

        db.session.add(usuario)

    db.session.commit()

    print(f"Usuarios creados correctamente: {Usuario.query.count()}")