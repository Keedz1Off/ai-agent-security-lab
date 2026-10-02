"""LLM03: Ненадёжные зависимости. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hashlib

# Фиктивный артефакт и заранее одобренный эталон.
approved = b"reviewed-demo-component-v1"
trusted_digest = hashlib.sha256(approved).hexdigest()
downloaded = b"reviewed-demo-component-v1"
if hashlib.sha256(downloaded).hexdigest() != trusted_digest:
    raise ValueError("STOP: файл изменился")
print("Файл совпадает с одобренным")
