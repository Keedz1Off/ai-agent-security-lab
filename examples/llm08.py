"""LLM08: Чужие документы в поиске. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# tenant берётся из проверенной сервером сессии.
tenant = "team-a"
chunks = [
    {"tenant": "team-a", "text": "Наш документ"},
    {"tenant": "team-b", "text": "Документ другой команды"},
]
# Сначала доступ, потом поиск внутри разрешённых данных.
allowed = [c for c in chunks if c["tenant"] == tenant]
hits = [c["text"] for c in allowed if "документ" in c["text"].lower()]
assert hits == ["Наш документ"]
print(hits)
