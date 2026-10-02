"""LLM07: Утечка системного промпта. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Ни ключа, ни пароля в сообщениях модели.
system_prompt = "Кратко объясняй учебные отчёты."
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Объясни результат: status=ok"},
]
print(messages)
# Ключи для внешних сервисов использует серверный адаптер.
# Его настройки не добавляются в messages.
