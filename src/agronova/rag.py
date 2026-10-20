"""Mini sistema de recuperación (la 'R' de RAG) sin modelos ni internet.

NO es un RAG completo: no usa embeddings ni un LLM. Sirve para ver, con código, cuatro ideas:
  1) los permisos se filtran ANTES de ordenar y de construir el contexto;
  2) cada respuesta cita su fuente;
  3) si no hay evidencia suficiente, el sistema se abstiene;
  4) la calidad se mide con preguntas de prueba (relevancia, abstención y fugas de permisos).
"""
import csv
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ROLES = {"operaciones": {"general"}, "compras": {"general", "compras"},
         "finanzas": {"general", "finanzas"}}
PARADAS = {"que", "cual", "cuales", "como", "quien", "del", "los", "las", "una", "uno", "por",
           "para", "con", "sus", "tus", "este", "esta"}
UMBRAL = 0.34   # proporción mínima de términos de la pregunta presentes en el fragmento


def _normalizar(texto):
    sin_tildes = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in sin_tildes if unicodedata.category(c) != "Mn")


def terminos(texto):
    salida = set()
    for t in re.findall(r"[a-z0-9]+", _normalizar(texto)):
        if len(t) < 3 or t in PARADAS:
            continue
        if len(t) > 4 and t.endswith("es"):
            t = t[:-2]
        elif len(t) > 4 and t.endswith("s"):
            t = t[:-1]
        salida.add(t)
    return salida


def cargar_fragmentos(carpeta=RAIZ / "rag" / "corpus"):
    """Un fragmento por párrafo, con metadatos (fuente y nivel de acceso)."""
    fragmentos = []
    for ruta in sorted(Path(carpeta).glob("*.md")):
        cabecera, _, cuerpo = ruta.read_text(encoding="utf-8").partition("---")
        meta = dict(l.split(":", 1) for l in cabecera.strip().splitlines())
        for parrafo in [p.strip() for p in cuerpo.split("\n\n") if p.strip()]:
            fragmentos.append({"fuente": ruta.name, "acceso": meta["acceso"].strip(),
                               "texto": parrafo, "terminos": terminos(parrafo)})
    return fragmentos


def recuperar(pregunta, rol, fragmentos, k=3):
    permitidos = ROLES[rol]
    candidatos = [f for f in fragmentos if f["acceso"] in permitidos]   # filtro ANTES de ordenar
    q = terminos(pregunta)
    if not q:
        return []
    puntuados = [(len(q & f["terminos"]) / len(q), f) for f in candidatos]
    puntuados = [(p, f) for p, f in puntuados if p >= UMBRAL]
    return sorted(puntuados, key=lambda x: -x[0])[:k]


def responder(pregunta, rol, fragmentos):
    """Respuesta extractiva: devuelve el mejor fragmento con su cita, o se abstiene."""
    encontrados = recuperar(pregunta, rol, fragmentos)
    if not encontrados:
        return {"abstiene": True, "respuesta": None, "citas": []}
    mejor = encontrados[0][1]
    return {"abstiene": False, "respuesta": mejor["texto"], "citas": [mejor["fuente"]]}


def evaluar(ruta=RAIZ / "rag" / "preguntas_prueba.csv"):
    fragmentos = cargar_fragmentos()
    with open(ruta, encoding="utf-8", newline="") as f:
        filas = list(csv.DictReader(f))
    resp = [(f, responder(f["pregunta"], f["rol"], fragmentos)) for f in filas]
    si = [(f, r) for f, r in resp if f["respondible"] == "si"]
    no = [(f, r) for f, r in resp if f["respondible"] == "no"]
    acceso = {f["fuente"]: f["acceso"] for f in fragmentos}
    return {
        "relevancia": sum(r["citas"] == [f["fuente_esperada"]] for f, r in si) / len(si),
        "abstencion_apropiada": sum(r["abstiene"] for f, r in no) / len(no),
        "fugas_de_permisos": sum(acceso[c] not in ROLES[f["rol"]] for f, r in resp for c in r["citas"]),
        "preguntas": len(filas),
    }


if __name__ == "__main__":
    for clave, valor in evaluar().items():
        print(f"{clave}: {valor}")
