from app.routes.actividad_cognitiva.baremos import BAREMOS, calcular_z_score


def aplicar_baremo(registro, campo_raw, campo_z, campo_percentil, campo_estimacion):
    valor = getattr(registro, campo_raw, None)

    if valor is None:
        return

    baremo = BAREMOS.get(campo_raw)

    idioma = registro.idioma or "spanish"
    if idioma not in ["spanish", "english"]:
        idioma = "spanish"

    coef = baremo[idioma]

    if not baremo:
        return

    resultado = calcular_z_score(
        raw_score=valor,
        intercept=coef["intercept"],
        edad=registro.edad,
        escolaridad=registro.escolaridad_anios,
        sexo=registro.sexo,
        beta_edad=coef["beta_edad"],
        beta_escolaridad=coef["beta_escolaridad"],
        beta_sexo=coef["beta_sexo"],
        rmse=coef["rmse"],
        score_invertido=baremo["invertido"]
    )

    setattr(registro, campo_z, resultado["z_score"])
    setattr(registro, campo_percentil, resultado["percentil"])
    setattr(registro, campo_estimacion, resultado["clasificacion"])


def calcular_indices_derivados(registro):
    # Trail diferencial: B - A
    if registro.trail_a_tiempo is not None and registro.trail_b_tiempo is not None:
        registro.trail_diferencial = round(
            registro.trail_b_tiempo - registro.trail_a_tiempo,
            2
        )

        if registro.trail_a_tiempo > 0:
            registro.trail_ratio = round(
                registro.trail_b_tiempo / registro.trail_a_tiempo,
                2
            )

    # Fluencia P + M
    if registro.fluencia_p is not None and registro.fluencia_m is not None:
        registro.fluencia_pm_total = registro.fluencia_p + registro.fluencia_m

    # Diferencia semántica - fonológica
    if (
        registro.fluidez_animales is not None
        and registro.fluidez_vegetales is not None
        and registro.fluencia_pm_total is not None
    ):
        semantica_total = registro.fluidez_animales + registro.fluidez_vegetales

        registro.fluencia_semantica_fonologica_diferencial = round(
            semantica_total - registro.fluencia_pm_total,
            2
        )

    # Benson porcentaje retenido
    if (
        registro.benson_copia_total is not None
        and registro.benson_recuerdo_total is not None
        and registro.benson_copia_total > 0
    ):
        registro.benson_porcentaje_retenido = round(
            (registro.benson_recuerdo_total / registro.benson_copia_total) * 100,
            2
        )

    # Craft porcentaje retenido
    if (
        registro.craft_inmediato_parafraseo is not None
        and registro.craft_diferido_parafraseo is not None
        and registro.craft_inmediato_parafraseo > 0
    ):
        registro.craft_porcentaje_retenido = round(
            (registro.craft_diferido_parafraseo / registro.craft_inmediato_parafraseo) * 100,
            2
        )

    # Diferencia verbal - visual
    if (
        registro.craft_porcentaje_retenido is not None
        and registro.benson_porcentaje_retenido is not None
    ):
        registro.diferencia_retencion_verbal_visual = round(
            registro.craft_porcentaje_retenido - registro.benson_porcentaje_retenido,
            2
        )

    # Índice de errores
    errores = [
        registro.trail_a_errores,
        registro.trail_b_errores,
    ]

    errores_validos = [e for e in errores if e is not None]

    if errores_validos:
        registro.indice_errores = sum(errores_validos)


def calcular_sueno(registro):
    if registro.sueno_indice_calidad is None:
        return

    valor = registro.sueno_indice_calidad

    if valor <= 5:
        registro.sueno_estimacion = "Calidad de sueño adecuada"
    elif valor <= 10:
        registro.sueno_estimacion = "Alteración leve del sueño"
    elif valor <= 15:
        registro.sueno_estimacion = "Alteración moderada del sueño"
    else:
        registro.sueno_estimacion = "Alteración severa del sueño"

def generar_perfil_cognitivo(registro):
    dominios = {
        "Atención y memoria de trabajo": [],
        "Función ejecutiva": [],
        "Lenguaje y acceso léxico": [],
        "Fluidez semántica": [],
        "Memoria visual": [],
        "Memoria verbal": [],
        "Sueño": [],
    }

    def bajo(percentil):
        return percentil is not None and percentil < 9

    def promedio_bajo(percentil):
        return percentil is not None and 9 <= percentil < 25

    def conservado(percentil):
        return percentil is not None and percentil >= 25

    # Atención
    if bajo(registro.digitos_inversos_total_percentil):
        dominios["Atención y memoria de trabajo"].append(
            "Bajo rendimiento en dígitos inversos, compatible con dificultad en memoria de trabajo."
        )
    elif promedio_bajo(registro.digitos_inversos_total_percentil):
        dominios["Atención y memoria de trabajo"].append(
            "Rendimiento bajo-promedio en memoria de trabajo."
        )

    # Función ejecutiva
    if bajo(registro.trail_b_percentil):
        dominios["Función ejecutiva"].append(
            "Bajo rendimiento en Trail Making Test B, compatible con dificultad en flexibilidad cognitiva."
        )
    elif promedio_bajo(registro.trail_b_percentil):
        dominios["Función ejecutiva"].append(
            "Rendimiento bajo-promedio en flexibilidad cognitiva."
        )

    if bajo(registro.trail_ratio_percentil):
        dominios["Función ejecutiva"].append(
            "El índice Trail B/A sugiere incremento del costo ejecutivo respecto a la velocidad de procesamiento."
        )

    # Lenguaje
    if bajo(registro.mint_32_percentil):
        dominios["Lenguaje y acceso léxico"].append(
            "Bajo rendimiento en denominación MINT-32, compatible con dificultad en acceso léxico o red semántica."
        )
    elif promedio_bajo(registro.mint_32_percentil):
        dominios["Lenguaje y acceso léxico"].append(
            "Rendimiento bajo-promedio en denominación."
        )

    # Fluidez semántica
    if bajo(registro.fluidez_animales_percentil):
        dominios["Fluidez semántica"].append(
            "Bajo rendimiento en categoría animales, compatible con dificultad en organización semántica."
        )

    if bajo(registro.fluidez_vegetales_percentil):
        dominios["Fluidez semántica"].append(
            "Bajo rendimiento en categoría vegetales."
        )

    if (
        conservado(registro.fluencia_pm_percentil)
        and (
            bajo(registro.fluidez_animales_percentil)
            or bajo(registro.fluidez_vegetales_percentil)
        )
    ):
        dominios["Fluidez semántica"].append(
            "La fluencia fonológica se conserva relativamente mejor que la semántica, lo que puede sugerir mayor compromiso de redes semánticas."
        )

    # Memoria visual
    if bajo(registro.benson_retencion_percentil):
        dominios["Memoria visual"].append(
            "Bajo porcentaje de retención visual en Benson, compatible con dificultad en memoria visual."
        )

    if bajo(registro.benson_copia_percentil):
        dominios["Memoria visual"].append(
            "Bajo rendimiento en copia de Benson, compatible con dificultad visoconstructiva o de planificación gráfica."
        )

    # Memoria verbal
    if bajo(registro.craft_retencion_percentil):
        dominios["Memoria verbal"].append(
            "Bajo porcentaje de retención verbal en Craft Story, compatible con dificultad en memoria episódica verbal."
        )

    if bajo(registro.craft_diferido_parafraseo_percentil):
        dominios["Memoria verbal"].append(
            "Bajo rendimiento en recuerdo diferido por parafraseo, sugerente de dificultad en recuperación o consolidación de información verbal."
        )

    # Sueño
    if registro.sueno_estimacion:
        dominios["Sueño"].append(registro.sueno_estimacion)

    partes = []

    for dominio, hallazgos in dominios.items():
        if hallazgos:
            partes.append(f"{dominio}: " + " ".join(hallazgos))

    if not partes:
        registro.perfil_cognitivo = (
            "El perfil general se encuentra dentro de rangos esperados en las áreas evaluadas, "
            "considerando edad, sexo, escolaridad e idioma."
        )
        registro.estimacion_global = "Promedio"
    else:
        registro.perfil_cognitivo = " ".join(partes)

        dominios_afectados = sum(1 for hallazgos in dominios.values() if hallazgos)

        if dominios_afectados >= 3:
            registro.estimacion_global = "Perfil con alteraciones en múltiples dominios"
        elif dominios_afectados == 2:
            registro.estimacion_global = "Perfil con alteraciones focales"
        else:
            registro.estimacion_global = "Perfil con hallazgo específico"

from app.routes.actividad_cognitiva.baremos import z_a_percentil, clasificar_percentil


def sexo_excel(valor):
    return 1 if valor == "femenino" else 0


def idioma_excel(valor):
    return 1 if valor == "spanish" else 0


def calcular_norma_excel(raw, edad, escolaridad, sexo, idioma, english, spanish, invertido=False):
    if raw is None:
        return None

    sexo_valor = sexo_excel(sexo)

    if idioma_excel(idioma) == 0:
        intercept, beta_edad, beta_edu, beta_sexo, rmse = english
    else:
        intercept, beta_edad, beta_edu, beta_sexo, rmse = spanish

    esperado = (
        intercept
        + (beta_edad * (edad or 0))
        + (beta_edu * (escolaridad or 0))
        + (beta_sexo * sexo_valor)
    )

    z = (raw - esperado) / rmse

    if invertido:
        z = -1 * z

    percentil = z_a_percentil(z)

    return {
        "z": round(z, 3),
        "percentil": round(percentil, 2),
        "estimacion": clasificar_percentil(percentil),
    }


def calcular_moca_excel(registro):
    resultado = calcular_norma_excel(
        raw=registro.moca_total,
        edad=registro.edad,
        escolaridad=registro.escolaridad_anios,
        sexo=registro.sexo,
        idioma=registro.idioma,
        english=(24.26963652, -0.09151608, 0.423868193, 0.579429049, 2.876818483),
        spanish=(26.04894366, -0.12845967, 0.498599857, -0.72423483, 3.682332412),
        invertido=False
    )

    if resultado:
        registro.moca_z = resultado["z"]
        registro.moca_percentil = resultado["percentil"]
        registro.moca_estimacion = resultado["estimacion"]


def calcular_trail_a_excel(registro):
    resultado = calcular_norma_excel(
        raw=registro.trail_a_tiempo,
        edad=registro.edad,
        escolaridad=registro.escolaridad_anios,
        sexo=registro.sexo,
        idioma=registro.idioma,
        english=(5.74978224, 0.513953514, -0.45621524, -2.61491419, 11.79286037),
        spanish=(19.28636074, 0.78653138, -2.27641051, 6.893267704, 27.44635477),
        invertido=True
    )

    if resultado:
        registro.trail_a_z = resultado["z"]
        registro.trail_a_percentil = resultado["percentil"]


def calcular_trail_b_excel(registro):
    resultado = calcular_norma_excel(
        raw=registro.trail_b_tiempo,
        edad=registro.edad,
        escolaridad=registro.escolaridad_anios,
        sexo=registro.sexo,
        idioma=registro.idioma,
        english=(115.33603306960866,1.0137509359627677,-5.132144447102201,-12.591021530016173,51.02352773399597),
        spanish=(132.2426025352612,1.7042862467287079,-8.650262231180148,25.126828084487865,73.51425474348872),
        
        invertido=True
    )

    if resultado:
        registro.trail_b_z = resultado["z"]
        registro.trail_b_percentil = resultado["percentil"]


def calcular_mint_excel(registro):
    resultado = calcular_norma_excel(
        raw=registro.mint_32_total,
        edad=registro.edad,
        escolaridad=registro.escolaridad_anios,
        sexo=registro.sexo,
        idioma=registro.idioma,
        english=(25.11989378, 0.003747736, 0.231637751, -0.779620158, 2.864949873),
        spanish=(30.91769739, -0.05267551, 0.123553401, -0.649551584, 2.437433601),
        invertido=False
    )

    if resultado:
        registro.mint_32_z = resultado["z"]
        registro.mint_32_percentil = resultado["percentil"]
        registro.mint_32_estimacion = resultado["estimacion"]

def calcular_actividad_cognitiva(registro):
    calcular_indices_derivados(registro)
    
    calcular_moca_excel(registro)
    calcular_trail_a_excel(registro)
    calcular_trail_b_excel(registro)
    calcular_mint_excel(registro)    


    aplicar_baremo(
        registro,
        "digitos_directos_total",
        "digitos_directos_total_z",
        "digitos_directos_total_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "digitos_directos_longitud",
        "digitos_directos_longitud_z",
        "digitos_directos_longitud_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "digitos_inversos_total",
        "digitos_inversos_total_z",
        "digitos_inversos_total_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "digitos_inversos_longitud",
        "digitos_inversos_longitud_z",
        "digitos_inversos_longitud_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluencia_p",
        "fluencia_p_z",
        "fluencia_p_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluencia_m",
        "fluencia_m_z",
        "fluencia_m_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluencia_pm_total",
        "fluencia_pm_z",
        "fluencia_pm_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluidez_animales",
        "fluidez_animales_z",
        "fluidez_animales_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluidez_vegetales",
        "fluidez_vegetales_z",
        "fluidez_vegetales_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "benson_copia_total",
        "benson_copia_z",
        "benson_copia_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "benson_recuerdo_total",
        "benson_recuerdo_z",
        "benson_recuerdo_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "benson_porcentaje_retenido",
        "benson_retencion_z",
        "benson_retencion_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "craft_inmediato_textual",
        "craft_inmediato_textual_z",
        "craft_inmediato_textual_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "craft_inmediato_parafraseo",
        "craft_inmediato_parafraseo_z",
        "craft_inmediato_parafraseo_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "craft_diferido_textual",
        "craft_diferido_textual_z",
        "craft_diferido_textual_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "craft_diferido_parafraseo",
        "craft_diferido_parafraseo_z",
        "craft_diferido_parafraseo_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "craft_porcentaje_retenido",
        "craft_retencion_z",
        "craft_retencion_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "trail_diferencial",
        "trail_diferencial_z",
        "trail_diferencial_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "trail_ratio",
        "trail_ratio_z",
        "trail_ratio_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "fluencia_semantica_fonologica_diferencial",
        "fluencia_semantica_fonologica_z",
        "fluencia_semantica_fonologica_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "indice_errores",
        "indice_errores_z",
        "indice_errores_percentil",
        "estimacion_global"
    )

    aplicar_baremo(
        registro,
        "diferencia_retencion_verbal_visual",
        "diferencia_retencion_verbal_visual_z",
        "diferencia_retencion_verbal_visual_percentil",
        "estimacion_global"
    )

    generar_perfil_cognitivo(registro)
    calcular_sueno(registro)


def calcular_estimaciones(registro):
    return calcular_actividad_cognitiva(registro)