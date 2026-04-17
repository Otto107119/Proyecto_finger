from flask_login import current_user


def puede_editar_area(usuario, area):
    if not usuario.is_authenticated:
        return False

    if usuario.rol == 'admin':
        return True

    if usuario.rol == 'gerontologia':
        return area == "historial_clinico"

    if usuario.rol in ['capturista', 'responsable']:
        return usuario.area == area

    return False


def puede_ver_area(usuario, area):
    if not usuario.is_authenticated:
        return False

    if usuario.rol in ['admin', 'gerontologia', 'capturista', 'responsable']:
        return True

    return False
