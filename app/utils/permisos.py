from flask_login import current_user


def es_superadmin(usuario=None):
    usuario = usuario or current_user

    return (
        usuario.is_authenticated
        and usuario.rol == "superadmin"
    )


def es_admin_area(usuario, area):
    return (
        usuario.is_authenticated
        and usuario.rol == "admin"
        and usuario.area == area
    )


def es_capturista_area(usuario, area):
    return (
        usuario.is_authenticated
        and usuario.rol == "capturista"
        and usuario.area == area
    )


def puede_ver_area(usuario, area):
    if not usuario.is_authenticated:
        return False

    return (
        es_superadmin(usuario)
        or es_admin_area(usuario, area)
        or es_capturista_area(usuario, area)
    )


def puede_crear_area(usuario, area):
    return puede_ver_area(usuario, area)


def puede_editar_area(usuario, area):
    return puede_ver_area(usuario, area)


def puede_eliminar_area(usuario, area):
    if not usuario.is_authenticated:
        return False

    return (
        es_superadmin(usuario)
        or es_admin_area(usuario, area)
    )


def puede_descargar_pdf_area(usuario, area):
    if not usuario.is_authenticated:
        return False

    return (
        es_superadmin(usuario)
        or es_admin_area(usuario, area)
    )


def puede_generar_respaldo(usuario=None):
    usuario = usuario or current_user

    return (
        usuario.is_authenticated
        and usuario.rol == "superadmin"
    )


def puede_gestionar_usuarios(usuario=None):
    usuario = usuario or current_user

    return (
        usuario.is_authenticated
        and usuario.rol in ["superadmin", "admin"]
    )