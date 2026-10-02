"""LLM09: Уверенная выдумка. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Фиктивные проверенные факты; свободную генерацию здесь не используем.
facts = {"report-1": {"count": 12}}
source_id = "report-1"
record = facts.get(source_id)
if record is None:
    answer = "Нет подтверждённых данных"
else:
    answer = f"Количество: {record['count']} (источник: {source_id})"
print(answer)
