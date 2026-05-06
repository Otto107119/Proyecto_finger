from flask import Blueprint

actividad_social_bp = Blueprint(
    "actividad_social",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/actividad_social"
)

from . import routes
from . import pdf