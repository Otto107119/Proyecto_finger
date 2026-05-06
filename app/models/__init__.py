from .usuario import Usuario
from .paciente import Paciente
from .actividad_fisica import ActividadFisica
from .actividad_cognitiva import ActividadCognitiva
from .actividad_nutricional import ActividadNutricional
from .area_medica import AreaMedica
from app.models.actividad_cognitiva import ActividadCognitiva
from app.models.actividad_fisica import ActividadFisica

from .actividad_social import (
    ActividadSocial,
    ActividadSocialEconomia,
    ActividadSocialPadreMadre,
    ActividadSocialHermano,
    ActividadSocialHijo,
)
from .historial_clinico import (
    HistorialClinico,
    ParesCraneales,
    MarchaEquilibrio,
    APHF,
    APPResumen,
    APPPatologia,
    FactoresRiesgo,
    EstudioComplementario,
    VisitaEspecialista,
)