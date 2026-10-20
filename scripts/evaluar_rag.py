"""Atajo multiplataforma:  python scripts/evaluar_rag.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agronova.rag import evaluar  # noqa: E402

for clave, valor in evaluar().items():
    print(f"{clave}: {valor}")
