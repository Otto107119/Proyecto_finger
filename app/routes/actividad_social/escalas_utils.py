def calcular_gds15_total(respuestas):
    """
    respuestas: dict con p1...p15 = 'si' o 'no'
    """
    claves_si_suman = ["p2", "p3", "p4", "p6", "p8", "p9", "p10", "p12", "p14", "p15"]
    claves_no_suman = ["p1", "p5", "p7", "p11", "p13"]

    total = 0

    for clave in claves_si_suman:
        if respuestas.get(clave) == "si":
            total += 1

    for clave in claves_no_suman:
        if respuestas.get(clave) == "no":
            total += 1

    return total


def interpretar_gds15(total):
    if total is None:
        return "Sin calcular"

    if total <= 4:
        return "Normal"

    return "Presencia de síntomas depresivos"


def calcular_katz_total(*valores):
    total = 0

    for valor in valores:
        try:
            total += int(valor)
        except (TypeError, ValueError):
            pass

    return total


def interpretar_katz(total):
    if total is None:
        return "Sin calcular"

    if total == 6:
        return "Independencia total"

    return "Dependencia"


def calcular_lawton_total(*valores):
    total = 0

    for valor in valores:
        try:
            total += int(valor)
        except (TypeError, ValueError):
            pass

    return total


def interpretar_lawton(total):
    if total is None:
        return "Sin calcular"

    if total == 21:
        return "Independiente"

    if 15 <= total <= 20:
        return "Dependencia leve"

    if 8 <= total <= 14:
        return "Dependencia moderada"

    return "Dependencia severa"