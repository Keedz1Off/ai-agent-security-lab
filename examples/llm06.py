"""LLM06: Слишком много полномочий. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab import GuardedSession, Scope

# Права задаёт приложение по задаче пользователя.
session = GuardedSession(Scope("report"))
text = session.read({
    "tool": "read_document",
    "document_id": "report",
})
print(text)  # Сессия предоставляет только разрешённое чтение.
