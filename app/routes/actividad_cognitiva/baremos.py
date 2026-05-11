from scipy.stats import norm


# =====================================================
# CONVERSIÓN
# =====================================================

def z_a_percentil(z_score):
    """
    Convierte z-score a percentil.
    """
    return round(norm.cdf(z_score) * 100, 2)


# =====================================================
# CLASIFICACIÓN CLÍNICA
# =====================================================

def clasificar_percentil(percentil):
    if percentil < 1:
        return "Severamente deteriorado"
    elif percentil < 2:
        return "Moderadamente deteriorado"
    elif percentil < 9:
        return "Levemente deteriorado"
    elif percentil < 25:
        return "Promedio bajo"
    elif percentil < 75:
        return "Promedio"
    elif percentil < 91:
        return "Promedio alto"
    elif percentil < 98:
        return "Superior"
    return "Muy superior"


# =====================================================
# CÁLCULO NORMATIVO GENERAL
# =====================================================

def calcular_z_score(
    raw_score,
    intercept,
    edad=None,
    escolaridad=None,
    sexo=None,
    beta_edad=0,
    beta_escolaridad=0,
    beta_sexo=0,
    rmse=1,
    score_invertido=False
):
    """
    Replica lógica del Excel UDS-3.

    Fórmula:

    esperado =
        intercept +
        (edad * beta_edad) +
        (escolaridad * beta_escolaridad) +
        (sexo * beta_sexo)

    z =
        (raw - esperado) / rmse

    score_invertido:
        usar para tiempos Trail A/B
        donde menor tiempo = mejor rendimiento.
    """

    sexo_valor = 1 if sexo == "femenino" else 0

    esperado = (
        intercept
        + ((edad or 0) * beta_edad)
        + ((escolaridad or 0) * beta_escolaridad)
        + (sexo_valor * beta_sexo)
    )

    z = (raw_score - esperado) / rmse

    # Trail A/B
    if score_invertido:
        z *= -1

    percentil = z_a_percentil(z)

    clasificacion = clasificar_percentil(percentil)

    return {
        "esperado": round(esperado, 3),
        "z_score": round(z, 3),
        "percentil": round(percentil, 2),
        "clasificacion": clasificacion
    }


# =====================================================
# BAREMOS UDS-3
# =====================================================

BAREMOS = {
    "moca_total": {
        "spanish": {
            "intercept": 26.0489436619,
            "beta_edad": -0.128459665,
            "beta_escolaridad": 0.498599857,
            "beta_sexo": -0.724234825,
            "rmse": 3.682332412,
        },
        "english": {
            "intercept": 24.269636522,
            "beta_edad": -0.091516076,
            "beta_escolaridad": 0.423868193,
            "beta_sexo": 0.579429049,
            "rmse": 2.876818483,
        },
        "invertido": False,
    },

    "digitos_directos_total": {
        "spanish": {"intercept": 4.177254023, "beta_edad": -0.005661849, "beta_escolaridad": 0.117718521, "beta_sexo": -0.22440612, "rmse": 1.627235531},
        "english": {"intercept": 3.741492063, "beta_edad": -0.00901272, "beta_escolaridad": 0.254508861, "beta_sexo": -0.010610052, "rmse": 2.297884927},
        "invertido": False,
    },

    "digitos_directos_longitud": {
        "spanish": {"intercept": 4.736440767, "beta_edad": -0.006416855, "beta_escolaridad": 0.06760014, "beta_sexo": -0.20867705, "rmse": 0.958479936},
        "english": {"intercept": 4.508761929, "beta_edad": -0.008195217, "beta_escolaridad": 0.126386071, "beta_sexo": 0.088763007, "rmse": 1.278250727},
        "invertido": False,
    },

    "digitos_inversos_total": {
        "spanish": {"intercept": 5.603957371, "beta_edad": -0.029841087, "beta_escolaridad": 0.114231179, "beta_sexo": -0.451353715, "rmse": 1.59055872},
        "english": {"intercept": 5.834425088, "beta_edad": -0.036583054, "beta_escolaridad": 0.17432335, "beta_sexo": 0.327640477, "rmse": 2.025801459},
        "invertido": False,
    },

    "digitos_inversos_longitud": {
        "spanish": {"intercept": 4.30936261, "beta_edad": -0.016854036, "beta_escolaridad": 0.0599246, "beta_sexo": -0.241445281, "rmse": 1.022418465},
        "english": {"intercept": 5.401786988, "beta_edad": -0.033111866, "beta_escolaridad": 0.091987642, "beta_sexo": 0.026916436, "rmse": 1.177194241},
        "invertido": False,
    },

    "trail_a_tiempo": {
        "spanish": {"intercept": 19.28636074, "beta_edad": 0.78653138, "beta_escolaridad": -2.276410512, "beta_sexo": 6.893267704, "rmse": 27.446354766},
        "english": {"intercept": 5.74978224, "beta_edad": 0.513953514, "beta_escolaridad": -0.456215238, "beta_sexo": -2.614914193, "rmse": 11.792860375},
        "invertido": True,
    },

    "trail_b_tiempo": {
        "spanish": {"intercept": 167.4444444, "beta_edad": 0, "beta_escolaridad": -9.45613305, "beta_sexo": 0, "rmse": 87.05320287},
        "english": {"intercept": 115.33603307, "beta_edad": 1.013750936, "beta_escolaridad": -5.132144447, "beta_sexo": -12.59102153, "rmse": 51.023527734},
        "invertido": True,
    },

    "mint_32_total": {
        "spanish": {"intercept": 30.917697394, "beta_edad": -0.052675505, "beta_escolaridad": 0.123553401, "beta_sexo": -0.649551584, "rmse": 2.437433601},
        "english": {"intercept": 25.119893778, "beta_edad": 0.003747736, "beta_escolaridad": 0.231637751, "beta_sexo": -0.779620158, "rmse": 2.864949873},
        "invertido": False,
    },

    "fluencia_p": {
        "spanish": {"intercept": 11.797272619, "beta_edad": -0.03095822, "beta_escolaridad": 0.297865867, "beta_sexo": -0.473193754, "rmse": 4.186729728},
        "english": {"intercept": 6.137072757, "beta_edad": -0.014412252, "beta_escolaridad": 0.487817191, "beta_sexo": 1.065193629, "rmse": 4.207065446},
        "invertido": False,
    },

    "fluencia_m": {
        "spanish": {"intercept": 9.227267163, "beta_edad": -0.026174152, "beta_escolaridad": 0.314382126, "beta_sexo": 0.290389385, "rmse": 4.093580118},
        "english": {"intercept": 6.198817737, "beta_edad": -0.042578365, "beta_escolaridad": 0.513167408, "beta_sexo": 1.483630805, "rmse": 4.025542573},
        "invertido": False,
    },

    "fluencia_pm_total": {
        "spanish": {"intercept": 21.386470892, "beta_edad": -0.064327839, "beta_escolaridad": 0.636898683, "beta_sexo": -0.181928046, "rmse": 7.690332567},
        "english": {"intercept": 12.684137761, "beta_edad": -0.058764954, "beta_escolaridad": 0.979081629, "beta_sexo": 2.592925842, "rmse": 7.530091136},
        "invertido": False,
    },

    "fluidez_animales": {
        "spanish": {"intercept": 26.682221171, "beta_edad": -0.165569784, "beta_escolaridad": 0.298668918, "beta_sexo": -0.138521766, "rmse": 4.195104028},
        "english": {"intercept": 20.926713696, "beta_edad": -0.103649535, "beta_escolaridad": 0.415943234, "beta_sexo": -0.209604694, "rmse": 4.530683401},
        "invertido": False,
    },

    "fluidez_vegetales": {
        "spanish": {"intercept": 13.754846347, "beta_edad": -0.074198176, "beta_escolaridad": 0.118040071, "beta_sexo": 2.817905737, "rmse": 3.550669643},
        "english": {"intercept": 9.661712786, "beta_edad": -0.015433473, "beta_escolaridad": 0.215530773, "beta_sexo": 2.664655795, "rmse": 3.471323644},
        "invertido": False,
    },
    
        "benson_copia_total": {
        "spanish": {"intercept": 14.979051694, "beta_edad": -0.013285819, "beta_escolaridad": 0.102788548, "beta_sexo": -0.396512365, "rmse": 1.780046271},
        "english": {"intercept": 17.695694843, "beta_edad": -0.041954107, "beta_escolaridad": 0.037485862, "beta_sexo": 0.148844077, "rmse": 1.301765488},
        "invertido": False,
    },

    "benson_recuerdo_total": {
        "spanish": {"intercept": 15.53186665, "beta_edad": -0.085011622, "beta_escolaridad": 0.177883193, "beta_sexo": -1.017089531, "rmse": 2.826915928},
        "english": {"intercept": 15.944881954, "beta_edad": -0.088447188, "beta_escolaridad": 0.109263904, "beta_sexo": -0.459810355, "rmse": 2.96857183},
        "invertido": False,
    },

    "craft_inmediato_textual": {
        "spanish": {"intercept": 15.174600903, "beta_edad": -0.03628212, "beta_escolaridad": 0.350699139, "beta_sexo": -0.461103671, "rmse": 5.808767742},
        "english": {"intercept": 15.818261507, "beta_edad": -0.100993516, "beta_escolaridad": 0.621497855, "beta_sexo": 2.899174089, "rmse": 6.319428165},
        "invertido": False,
    },

    "craft_inmediato_parafraseo": {
        "spanish": {"intercept": 13.023651646, "beta_edad": -0.041988937, "beta_escolaridad": 0.268512579, "beta_sexo": -0.48167913, "rmse": 4.161050944},
        "english": {"intercept": 11.987365695, "beta_edad": -0.068298232, "beta_escolaridad": 0.442838745, "beta_sexo": 1.550972747, "rmse": 3.72797303},
        "invertido": False,
    },

    "craft_diferido_textual": {
        "spanish": {"intercept": 11.737025547, "beta_edad": -0.017702205, "beta_escolaridad": 0.355766142, "beta_sexo": -1.041599904, "rmse": 5.448203125},
        "english": {"intercept": 16.27310898, "beta_edad": -0.084901819, "beta_escolaridad": 0.391607648, "beta_sexo": 2.242793518, "rmse": 6.405354696},
        "invertido": False,
    },

    "craft_diferido_parafraseo": {
        "spanish": {"intercept": 13.635648948, "beta_edad": -0.057971156, "beta_escolaridad": 0.239400516, "beta_sexo": -0.601901156, "rmse": 4.089730827},
        "english": {"intercept": 11.652392219, "beta_edad": -0.052897259, "beta_escolaridad": 0.34300236, "beta_sexo": 1.463919048, "rmse": 4.097460169},
        "invertido": False,
    },

    "trail_diferencial": {
        "spanish": {"intercept": 106.852859993, "beta_edad": 1.12969249, "beta_escolaridad": -7.076841235, "beta_sexo": 19.722623739, "rmse": 62.416277314},
        "english": {"intercept": 109.150473196, "beta_edad": 0.515194398, "beta_escolaridad": -4.711225721, "beta_sexo": -9.981057649, "rmse": 46.723894668},
        "invertido": True,
    },

    "trail_ratio": {
        "spanish": {"intercept": 2.966743475,"beta_edad": 0.006634504,"beta_escolaridad": 0,"beta_sexo": 0,"rmse": 1.526006398},
        "english": {"intercept": 6.238898592, "beta_edad": -0.017598273, "beta_escolaridad": -0.118225312, "beta_sexo": -0.129416058, "rmse": 1.366506679},
        "invertido": True,
    },

    "fluencia_semantica_fonologica_diferencial": {
        "spanish": {"intercept": 21.081587357, "beta_edad": -0.201503564, "beta_escolaridad": -0.241619009, "beta_sexo": 2.741924448, "rmse": 7.359340153},
        "english": {"intercept": 16.062369597, "beta_edad": -0.03496109, "beta_escolaridad": -0.336782543, "beta_sexo": -0.224837878, "rmse": 7.601175406},
        "invertido": False,
    },

    "indice_errores": {
        "spanish": {"intercept": 0.411214166,"beta_edad": 0.04407566,"beta_escolaridad": 0,"beta_sexo": 0,"rmse": 3.037478791},
        "english": {"intercept": 3.54192199, "beta_edad": 0.012683131, "beta_escolaridad": -0.097803623, "beta_sexo": -0.367124836, "rmse": 2.467580751},
        "invertido": True,
    },

    "craft_porcentaje_retenido": {
        "spanish": {"intercept": 75.134160313, "beta_edad": 0.123951497, "beta_escolaridad": 0.282071162, "beta_sexo": -3.039477765, "rmse": 20.735489392},
        "english": {"intercept": 88.251507372, "beta_edad": 0.157517153, "beta_escolaridad": -0.627269868, "beta_sexo": -1.090031898, "rmse": 19.00938749},
        "invertido": False,
    },

    "benson_porcentaje_retenido": {
        "spanish": {"intercept": 102.424988532, "beta_edad": -0.492238287, "beta_escolaridad": 0.723606963, "beta_sexo": -4.730247292, "rmse": 18.903141077},
        "english": {"intercept": 92.863556226, "beta_edad": -0.383028107, "beta_escolaridad": 0.53935949, "beta_sexo": -3.594771208, "rmse": 18.187851248},
        "invertido": False,
    },

    "diferencia_retencion_verbal_visual": {
        "spanish": {"intercept": -24.509608207, "beta_edad": 0.5941095, "beta_escolaridad": -0.488284251, "beta_sexo": 1.021184172, "rmse": 26.888151235},
        "english": {"intercept": 3.174302482, "beta_edad": 0.487476473, "beta_escolaridad": -1.348813216, "beta_sexo": 0.318203799, "rmse": 26.066078368},
        "invertido": False,
    },
}
# Alias para mantener compatibilidad con routes.py
def calcular_estimaciones(registro):
    return calcular_actividad_cognitiva(registro)