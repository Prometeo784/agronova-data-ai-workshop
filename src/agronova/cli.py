"""Línea de comandos de la mini plataforma.

  python -m agronova simular --dias 6            # ejecuta 6 días sobre una base en memoria
  python -m agronova simular --db estado.db      # igual, pero guardando el estado en un archivo
  python -m agronova simular --dias 1 --regla-defectuosa --reprocesar
"""
import argparse

from .fuentes import crear_erp_simulado
from .plataforma import EsquemaOrigenError, abrir, ejecutar_corrida, gold, reprocesar_silver
from .simulador import DESCRIPCIONES, ahora_simulado, avanzar_dia


def simular(args):
    erp, dw = crear_erp_simulado(), abrir(args.db)
    for dia in range(1, args.dias + 1):
        if dia > 1:
            avanzar_dia(erp, dia)
        print(f"\nDía {dia}: {DESCRIPCIONES.get(dia, 'sin cambios')}")
        try:
            r = ejecutar_corrida(erp, dw, f"dia-{dia}", ahora_simulado(dia), regla_defectuosa=args.regla_defectuosa)
            print(f"  OK     leídas {r['leidas']:>5,} | Bronze {r['bronze']:,} | Silver {r['silver']:,} | "
                  f"Cuarentena {r['cuarentena']:,} ({r['pct_cuarentena']:.1%}) | alertas: {', '.join(r['alertas']) or 'ninguna'}")
        except EsquemaOrigenError as e:
            print(f"  FALLA  {e}  (la marca de agua no avanzó; el estado no cambió)")
    if args.reprocesar:
        r = reprocesar_silver(dw, "reproceso", ahora_simulado(args.dias))
        print(f"\nReproceso desde Bronze con la regla corregida: Silver {r['silver']:,} | Cuarentena {r['cuarentena']:,}")
    print("\nGold: OTD por proveedor")
    print(gold(dw).to_string())


def main(argv=None):
    p = argparse.ArgumentParser(prog="agronova", description="Mini plataforma didáctica (datos sintéticos)")
    sub = p.add_subparsers(dest="orden", required=True)
    s = sub.add_parser("simular", help="Simula días de operación")
    s.add_argument("--dias", type=int, default=6)
    s.add_argument("--db", default=":memory:")
    s.add_argument("--regla-defectuosa", action="store_true")
    s.add_argument("--reprocesar", action="store_true")
    s.set_defaults(funcion=simular)
    args = p.parse_args(argv)
    args.funcion(args)


if __name__ == "__main__":
    main()
