"""PLANTILLA (no probada aquí): consumir una API REST con paginación y reintentos.
La URL es ficticia. Requiere: requests."""
import os

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

sesion = requests.Session()
reintentos = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
sesion.mount("https://", HTTPAdapter(max_retries=reintentos))
sesion.headers["Authorization"] = f"Bearer {os.environ['LOGISTICA_TOKEN']}"

filas, pagina = [], 1
while True:
    r = sesion.get("https://api.ejemplo-logistica.test/envios", params={"page": pagina}, timeout=30)
    r.raise_for_status()
    datos = r.json()
    if not datos:
        break
    filas.extend(datos)
    pagina += 1

envios = pd.DataFrame(filas)
print(f"{len(envios):,} envíos")
