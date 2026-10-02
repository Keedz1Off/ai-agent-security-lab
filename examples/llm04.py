"""LLM04: Отравленные данные. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Метаданные выставляет наш процесс проверки, не автор записи.
rows = [
    {"text": "Проверенный пример", "source": "curated", "reviewed": True},
    {"text": "Непроверенный пример", "source": "unknown", "reviewed": False},
]
approved = [
    r["text"] for r in rows
    if r["source"] == "curated" and r["reviewed"] is True
]
assert approved == ["Проверенный пример"]
print(approved)
