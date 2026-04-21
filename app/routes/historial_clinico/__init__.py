from flask import Blueprint

historial_clinico_bp = Blueprint(
    "historial_clinico",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/historial-clinico"
)

from . import datos_generales
from . import area_social
from . import area_espiritual
from . import area_psicologica
from . import area_fisica
from . import pares_craneales