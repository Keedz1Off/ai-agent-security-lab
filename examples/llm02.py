"""LLM02: Утечка приватных данных. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# user_id приходит из проверенной сессии, а не из ответа ИИ.
user_id = "alice"
records = [
    {"owner": "alice", "text": "Мой учебный отчёт"},
    {"owner": "bob", "text": "Чужой учебный отчёт"},
]
context = [r["text"] for r in records if r["owner"] == user_id]
assert context == ["Мой учебный отчёт"]
print(context)
