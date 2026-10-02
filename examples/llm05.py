"""LLM05: Опасная обработка ответа. Только фиктивные данные."""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from lab import render_text

model_output = "<label>Учебный пример</label>"
safe_html = render_text(model_output)
assert "&lt;label&gt;" in safe_html
print(safe_html)
