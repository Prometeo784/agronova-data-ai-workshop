"""Atajo multiplataforma:  python scripts/ejecutar_pipeline.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agronova.pipeline import ejecutar  # noqa: E402

ejecutar()
