from statistics import median


def alerta_volumen(filas_hoy, historico, tolerancia=0.5):
    if not historico:
        return True            # sin referencia, conviene revisar
    base = median(historico)
    return abs(filas_hoy - base) > tolerancia * base
