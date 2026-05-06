def obtener_punto_corte(prueba):
    puntos = {
        "moca": "≥26 normal | 18-25 DCL | ≤17 demencia",
        "trail_a": ">78 seg: riesgo en atención sostenida",
        "trail_b": ">273 seg: déficit ejecutivo severo",
        "mint": "Depende de escolaridad",
        "fluencia_pm": ">13 normal | 9-12 leve | <8 moderado/severo",
        "animales": "<12 palabras: alarma clínica",
        "vegetales": "<9 palabras: alarma clínica",
        "benson": "Interpretar según puntaje y retención",
        "craft": "Normal 15-16 | DCL 8-12 | Demencia 7-8",
    }

    return puntos.get(prueba, "-")


def generar_resumen_clinico(registro):
    hallazgos = []

    if registro.trail_a_estimacion and "Riesgo" in registro.trail_a_estimacion:
        hallazgos.append("compromiso en atención sostenida")

    if registro.trail_b_estimacion and "Déficit" in registro.trail_b_estimacion:
        hallazgos.append("alteración en función ejecutiva")

    if registro.mint_32_estimacion and registro.mint_32_estimacion != "Normal":
        hallazgos.append("alteración en búsqueda léxica")

    if registro.fluencia_estimacion and registro.fluencia_estimacion != "Normal":
        hallazgos.append("alteración en fluencia fonológica")

    if registro.fluidez_semantica_estimacion and "alarma" in registro.fluidez_semantica_estimacion.lower():
        hallazgos.append("alerta en fluidez semántica")

    if hallazgos:
        texto = "Se observa " + ", ".join(hallazgos) + ". "
    else:
        texto = "No se observan alteraciones cognitivas significativas en las áreas evaluadas. "

    porcentaje_craft = getattr(registro, "porcentaje_retenido_craft", None)
    if porcentaje_craft is None:
        porcentaje_craft = getattr(registro, "craft_porcentaje_retenido", None)

    porcentaje_benson = getattr(registro, "benson_porcentaje_retenido", None)
    if porcentaje_benson is None:
        porcentaje_benson = getattr(registro, "porcentaje_retenido_benson", None)

    if porcentaje_craft is not None:
        texto += f"Retención verbal Craft: {porcentaje_craft}%. "

    if porcentaje_benson is not None:
        texto += f"Retención visual Benson: {porcentaje_benson}%. "

    if registro.estimacion_global:
        texto += f"Perfil compatible con {registro.estimacion_global.lower()}."

    return texto