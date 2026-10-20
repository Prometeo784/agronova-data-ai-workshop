"""Atajo multiplataforma:  python scripts/simular_plataforma.py --dias 6"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from agronova.cli import main  # noqa: E402

main(["simular", *sys.argv[1:]])
