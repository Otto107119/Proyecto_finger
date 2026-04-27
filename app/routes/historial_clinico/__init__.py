from flask import Blueprint


historial_clinico_bp = Blueprint(
    "historial_clinico",
    __name__,
    url_prefix="/pacientes/<int:paciente_id>/historial-clinico"
)

from . import index
from . import datos_generales
from . import area_social
from . import area_espiritual
from . import area_psicologica
from . import area_fisica
from . import pares_craneales
from . import marcha_equilibrio
from . import aphf
from . import app
from . import factores_riesgo
from . import estudios_complementarios
from . import visitas_especialista
from . import resumen
from . import pdf