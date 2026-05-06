from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

usuarios = [

    # =========================
    # SUPERADMIN
    # =========================
    {
        "nombre": "Super Administrador",
        "correo": "superadmin@latam.com",
        "password": "123456",
        "rol": "superadmin",
        "area": None
    },

    # =========================
    # ADMINS
    # =========================
    {
        "nombre": "Admin Actividad Física",
        "correo": "admin.fisica@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "actividad_fisica"
    },

    {
        "nombre": "Admin Actividad Cognitiva",
        "correo": "admin.cognitiva@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "actividad_cognitiva"
    },

    {
        "nombre": "Admin Actividad Nutricional",
        "correo": "admin.nutricion@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "actividad_nutricional"
    },

    {
        "nombre": "Admin Área Médica",
        "correo": "admin.medica@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "area_medica"
    },

    {
        "nombre": "Admin Actividad Social",
        "correo": "admin.social@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "actividad_social"
    },

    {
        "nombre": "Admin Historial Clínico",
        "correo": "admin.historial@latam.com",
        "password": "123456",
        "rol": "admin",
        "area": "historial_clinico"
    },

    # =========================
    # CAPTURISTAS
    # =========================
    {
        "nombre": "Capturista Actividad Física",
        "correo": "capturista.fisica@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "actividad_fisica"
    },

    {
        "nombre": "Capturista Actividad Cognitiva",
        "correo": "capturista.cognitiva@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "actividad_cognitiva"
    },

    {
        "nombre": "Capturista Actividad Nutricional",
        "correo": "capturista.nutricion@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "actividad_nutricional"
    },

    {
        "nombre": "Capturista Área Médica",
        "correo": "capturista.medica@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "area_medica"
    },

    {
        "nombre": "Capturista Actividad Social",
        "correo": "capturista.social@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "actividad_social"
    },

    {
        "nombre": "Capturista Historial Clínico",
        "correo": "capturista.historial@latam.com",
        "password": "123456",
        "rol": "capturista",
        "area": "historial_clinico"
    },
]


with app.app_context():

    for data in usuarios:

        existente = Usuario.query.filter_by(
            correo=data["correo"]
        ).first()

        if existente:
            print(f"YA EXISTE: {data['correo']}")
            continue

        usuario = Usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            rol=data["rol"],
            area=data["area"]
        )

        usuario.set_password(data["password"])

        db.session.add(usuario)

        print(f"CREADO: {data['correo']}")

    db.session.commit()

    print("\nUsuarios creados correctamente.")