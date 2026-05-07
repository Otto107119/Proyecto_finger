def interpretar_gds(total):
    if total is None:
        return None

    if 0 <= total <= 4:
        return "Normal"
    if 5 <= total <= 8:
        return "Depresión leve"
    if 9 <= total <= 11:
        return "Depresión moderada"
    if 12 <= total <= 15:
        return "Depresión grave"

    return "Valor fuera de rango"


def calcular_katz_total(*valores):
    if not valores:
        return None

    contestadas = [v for v in valores if v in ["I", "A", "D"]]

    if not contestadas:
        return None

    return sum(1 for v in contestadas if v == "I")


def interpretar_katz(total):
    if total is None:
        return None

    if total == 6:
        return "Independencia total"

    return "Dependencia en una o más actividades"