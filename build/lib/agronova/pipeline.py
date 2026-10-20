"""Pipeline completo. Ejecutar:  PYTHONPATH=src python -m agronova.pipeline"""
import pandas as pd

from .control import reconciliar
from .fuentes import crear_erp_simulado, generar_inspecciones
from .gold import a_gold, calidad
from .ingesta import cargar_bronze, extraer_incremental
from .silver import a_silver


def _informe(r):
    print(f"  Bronze {r['bronze']:,} | Silver {r['silver']:,} | Cuarentena {r['cuarentena']:,}"
          f" ({r['pct_cuarentena']:.1%})  reconcilia: {'sí' if r['reconcilia'] else 'NO'}")
    if r["alerta"]:
        print("  ALERTA: la cuarentena supera el umbral. El proceso terminó sin errores,"
              " pero el dato puede estar mal.")


def ejecutar():
    erp, bronze = crear_erp_simulado(), pd.DataFrame()
    print("1) Carga inicial (sin marca de agua)")
    nuevos = extraer_incremental(erp, None)
    bronze = cargar_bronze(bronze, nuevos, "lote-001")
    marca = nuevos["fecha_modificacion"].max()
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,} | marca de agua {marca}")
    print("2) Segunda corrida: nada cambió en el ERP")
    nuevos = extraer_incremental(erp, marca)
    bronze = cargar_bronze(bronze, nuevos, "lote-002")
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,}")
    print("3) Re-ejecución con la marca reiniciada (deduplicación por clave en memoria)")
    nuevos = extraer_incremental(erp, None)
    bronze = cargar_bronze(bronze, nuevos, "lote-003")
    print(f"  Leídas {len(nuevos):,} | Bronze {len(bronze):,}  (sin duplicados)")
    print("4) Silver con la regla DEFECTUOSA (pipeline verde, dato incorrecto)")
    s_mal, c_mal = a_silver(bronze, regla_defectuosa=True)
    _informe(reconciliar(bronze, s_mal, c_mal))
    print("5) Silver con la regla CORREGIDA")
    silver, cuarentena = a_silver(bronze)
    _informe(reconciliar(bronze, silver, cuarentena))
    print("6) Gold: OTD por proveedor")
    print(a_gold(silver).to_string())
    ac, ins, yld = calidad(generar_inspecciones())
    print(f"7) Calidad: {ac:,} aceptadas / {ins:,} inspeccionadas = {yld:.1%}")
    return bronze, silver, cuarentena


if __name__ == "__main__":
    ejecutar()
