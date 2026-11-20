# AI Agent Security Lab

Учебный Python-проект про права ИИ-агента. Код ограничивает доступ к выбранному документу, проверяет имя инструмента, экранирует HTML и ограничивает число попыток.

**10 тестов** проверяют эти правила. Один из тестов перебирает 2 000 случайных действий с фиксированным seed. Для запуска хватает Python 3.11 и тестовых данных из репозитория.

## С чего начать

- [10 рисков ИИ простыми словами](docs/BASIC.md). Для первого просмотра подойдут карточки [про инструкции](docs/BASIC.md#llm01), [права агента](docs/BASIC.md#llm06) и [доступ к данным](docs/BASIC.md#llm02).
- [Правила доступа в коде](lab.py) · [Методика тестов](docs/TESTING.md)

## Запуск

Открой [Policy tests в GitHub Actions](https://github.com/Keedz1Off/ai-agent-security-lab/actions/workflows/checks.yml) и нажми **Run workflow**. CI сохраняет лог в `check-results`. Галочка **CD demo** добавляет архив `verified-delivery` с логом, SHA коммита и контрольной суммой.

Локально из папки проекта:

```sh
python -m unittest discover -s tests -v
```

Карточки опираются на [OWASP LLM Top 10 — 2025](https://genai.owasp.org/llm-top-10/). Тесты используют локальный код и вымышленные данные.
