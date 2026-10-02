"""LLM10: Бесконечные действия и расходы. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab import GuardedSession, Scope, DeniedAction

session = GuardedSession(Scope("report", max_calls=1))
request = {"tool": "read_document", "document_id": "report"}
session.read(request)
try:
    session.read(request)
except DeniedAction:
    print("STOP: лимит попыток исчерпан")
