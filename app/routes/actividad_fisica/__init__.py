from flask import Blueprint

actividad_fisica_bp = Blueprint(
    "actividad_fisica",
    __name__,
    url_prefix="/actividad-fisica"
)

from . import routes