def clasificar_moca(valor):
    if valor is None:
        return None

    if valor >= 26:
        return "Normal"
    elif 18 <= valor <= 25:
        return "Deterioro cognitivo leve"
    else:
        return "Probable demencia"


def clasificar_trail_a(tiempo):
    if tiempo is None:
        return None

    if tiempo <= 78:
        return "Rango esperado"
    return "Riesgo en atención sostenida"


def clasificar_trail_b(tiempo):
    if tiempo is None:
        return None

    if tiempo >= 273:
        return "Déficit ejecutivo severo"
    return "Sin déficit severo evidente"


def clasificar_mint(valor, escolaridad):
    if valor is None:
        return None

    if escolaridad is None:
        if valor >= 24:
            return "Rango aceptable"
        return "Riesgo en búsqueda léxica"

    if escolaridad <= 9:
        return "Normal" if valor >= 24 else "Riesgo en búsqueda léxica"

    if 10 <= escolaridad <= 15:
        return "Normal" if valor >= 27 else "Riesgo en búsqueda léxica"

    if escolaridad >= 16:
        return "Normal" if valor >= 29 else "Riesgo en búsqueda léxica"

    return None


def clasificar_fluencia(promedio):
    if promedio is None:
        return None

    if promedio > 13:
        return "Normal"
    elif 9 <= promedio <= 12:
        return "Deterioro leve"
    else:
        return "Deterioro moderado/severo"


def clasificar_semantica(animales, vegetales):
    alertas = []

    if animales is not None and animales < 12:
        alertas.append("baja fluidez en animales")

    if vegetales is not None and vegetales < 9:
        alertas.append("baja fluidez en vegetales")

    if not alertas:
        return "Sin alarma clínica evidente"

    return "Alarma clínica: " + ", ".join(alertas)


def porcentaje_retencion(diferido, inmediato):
    if diferido is None or inmediato in (None, 0):
        return None

    return round((diferido / inmediato) * 100, 2)


def calcular_estimaciones(registro):
    registro.moca_estimacion = clasificar_moca(registro.moca_total)

    registro.trail_a_estimacion = clasificar_trail_a(registro.trail_a_tiempo)
    registro.trail_b_estimacion = clasificar_trail_b(registro.trail_b_tiempo)

    registro.mint_32_estimacion = clasificar_mint(
        registro.mint_32_total,
        registro.escolaridad_anios
    )

    # 🔹 Fluencia fonológica
    if registro.fluencia_p is not None and registro.fluencia_m is not None:
        registro.fluencia_pm_promedio = round(
            (registro.fluencia_p + registro.fluencia_m) / 2,
            2
        )
    else:
        registro.fluencia_pm_promedio = None

    registro.fluencia_estimacion = clasificar_fluencia(
        registro.fluencia_pm_promedio
    )

    # 🔹 Fluidez semántica
    registro.fluidez_semantica_estimacion = clasificar_semantica(
        registro.animales_total,
        registro.vegetales_total
    )

    # 🔹 Retención
    registro.craft_porcentaje_retenido = porcentaje_retencion(
        registro.craft_rd_44,
        registro.craft_ri_44
    )

    registro.benson_porcentaje_retenido = porcentaje_retencion(
        registro.benson_diferida,
        registro.benson_inmediata
    )

    # 🔹 Diferencia verbal vs visual
    if registro.craft_porcentaje_retenido is not None and registro.benson_porcentaje_retenido is not None:
        registro.diferencia_retencion_verbal_visual = round(
            registro.craft_porcentaje_retenido - registro.benson_porcentaje_retenido,
            2
        )
    else:
        registro.diferencia_retencion_verbal_visual = None

    # 🔹 Trail (CORRECTO)
    if registro.trail_a_tiempo is not None and registro.trail_b_tiempo is not None:
        registro.trail_puntuacion_diferencial = round(
            registro.trail_b_tiempo - registro.trail_a_tiempo,
            2
        )

        if registro.trail_a_tiempo > 0:
            registro.trail_puntuacion_ratio = round(
                registro.trail_b_tiempo / registro.trail_a_tiempo,
                2
            )
        else:
            registro.trail_puntuacion_ratio = None
    else:
        registro.trail_puntuacion_diferencial = None
        registro.trail_puntuacion_ratio = None

    # 🔹 Resultado global (SIEMPRE fuera)
    registro.estimacion_global = generar_estimacion_global(registro)
    registro.resumen_automatico = generar_resumen_automatico(registro)


def generar_estimacion_global(registro):
    alertas = 0

    campos_alerta = [
        registro.moca_estimacion,
        registro.trail_a_estimacion,
        registro.trail_b_estimacion,
        registro.mint_32_estimacion,
        registro.fluencia_estimacion,
        registro.fluidez_semantica_estimacion
    ]

    for campo in campos_alerta:
        if campo and any(palabra in campo.lower() for palabra in ["riesgo", "deterioro", "déficit", "demencia", "alarma"]):
            alertas += 1

    if alertas == 0:
        return "Sin alteraciones cognitivas evidentes"
    elif alertas <= 2:
        return "Riesgo cognitivo leve"
    elif alertas <= 4:
        return "Riesgo cognitivo moderado"
    return "Riesgo cognitivo alto"


def generar_resumen_automatico(registro):
    resumen = []

    if registro.moca_estimacion:
        resumen.append(f"MOCA: {registro.moca_estimacion}.")

    if registro.trail_a_estimacion:
        resumen.append(f"Atención sostenida: {registro.trail_a_estimacion}.")

    if registro.trail_b_estimacion:
        resumen.append(f"Función ejecutiva: {registro.trail_b_estimacion}.")

    if registro.mint_32_estimacion:
        resumen.append(f"Búsqueda léxica: {registro.mint_32_estimacion}.")

    if registro.fluencia_estimacion:
        resumen.append(f"Fluencia fonológica: {registro.fluencia_estimacion}.")

    if registro.fluidez_semantica_estimacion:
        resumen.append(f"Fluidez semántica: {registro.fluidez_semantica_estimacion}.")

    if registro.craft_porcentaje_retenido is not None:
        resumen.append(f"Retención verbal Craft Story: {registro.craft_porcentaje_retenido}%.")

    if registro.benson_porcentaje_retenido is not None:
        resumen.append(f"Retención visual Benson: {registro.benson_porcentaje_retenido}%.")

    if registro.estimacion_global:
        resumen.append(f"Estimación global: {registro.estimacion_global}.")

    return " ".join(resumen)