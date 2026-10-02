"""LLM01: Подмена инструкций. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab import GuardedSession, Scope, DeniedAction

session = GuardedSession(Scope("report"))
# Имитируем предложение модели, а не реальную атаку.
proposal = {"tool": "unknown", "document_id": "report"}
try:
    session.read(proposal)
except DeniedAction:
    print("STOP: текст не может выдать новые права")
