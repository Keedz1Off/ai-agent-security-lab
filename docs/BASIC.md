# База: 10 рисков ИИ простым кодом

В каждом примере данные вымышлены. `tool()` только печатает действие: он ничего не отправляет, не удаляет и не открывает в сети.

<a id="llm01"></a>
## 01. Подмена документа / инструкции

**Проблема:** `report.txt` — недоверенный документ. В нём может быть фраза, похожая на команду для агента.

```text
report.txt с чужой командой -> ИИ -> tool() запускается
```

### Уязвимо

```python
def tool(action):
    print("Выполняю:", action)

report = open("report.txt", encoding="utf-8").read()
if "TOOL:" in report:
    tool(report.split("TOOL:")[1].strip())  # плохо
```

### Защита

```python
report = open("report.txt", encoding="utf-8").read()
user_task = "summarize"

if user_task == "summarize":
    print("Показываю текст отчёта:", report)
else:
    print("STOP: задача не разрешена")

# Текст report.txt остаётся просто текстом.
# Он не выбирает действие tool().
```

```text
report.txt -> ИИ -> if задача разрешена -> показать текст
                         иначе -> STOP
```

<a id="llm02"></a>
## 02. Чужой документ в ответе

**Проблема:** агент получил файлы всех пользователей и сам выбирает, что показать.

### Уязвимо

```python
files = {"alice.txt": "Отчёт Алисы", "bob.txt": "Отчёт Боба"}
requested_file = "bob.txt"
print(files[requested_file])  # плохо: можно выбрать чужой файл
```

### Защита

```python
user = "alice"
allowed_file = user + ".txt"
requested_file = "bob.txt"

if requested_file == allowed_file:
    print(files[requested_file])
else:
    print("STOP: это не твой документ")
```

```text
Запрос файла -> if это файл пользователя -> показать
                                  иначе -> STOP
```

<a id="llm03"></a>
## 03. Подмена библиотеки или модели

**Проблема:** файл скачался под знакомым именем, но его содержимое заменили.

### Уязвимо

```python
downloaded_file = b"unknown file"
load(downloaded_file)  # плохо: запускаем/подключаем без проверки
```

### Защита

```python
import hashlib

expected_hash = "7ad65a3053efbe417b3761f745c8a03ce47589172c304a486b686bf42330b9bf"
downloaded_file = b"reviewed file"
actual_hash = hashlib.sha256(downloaded_file).hexdigest()

if actual_hash == expected_hash:
    load(downloaded_file)
else:
    print("STOP: файл не совпадает с проверенной версией")
```

```text
Файл -> if хеш совпал -> подключить
                 иначе -> STOP
```

<a id="llm04"></a>
## 04. Подмена данных для обучения

**Проблема:** в набор попадает запись неизвестного происхождения.

### Уязвимо

```python
dataset = ["проверенная запись", "запись от неизвестного автора"]
train(dataset)  # плохо: всё сразу идёт в обучение
```

### Защита

```python
rows = [
    {"text": "проверенная запись", "reviewed": True},
    {"text": "неизвестная запись", "reviewed": False},
]

clean_dataset = []
for row in rows:
    if row["reviewed"] is True:
        clean_dataset.append(row["text"])
    else:
        print("STOP: запись не прошла проверку")

train(clean_dataset)
```

```text
Запись -> if проверена -> набор данных
                     иначе -> STOP
```

<a id="llm05"></a>
## 05. Ответ ИИ вставляется на страницу

**Проблема:** веб-страница принимает ответ ИИ как HTML-разметку.

### Уязвимо

```python
answer = "<b>Текст от ИИ</b>"
page.innerHTML = answer  # плохо: браузер читает это как HTML
```

### Защита

```python
answer = "<b>Текст от ИИ</b>"

if len(answer) <= 1000:
    page.textContent = answer  # браузер показывает обычный текст
else:
    print("STOP: ответ слишком большой")
```

```text
Ответ ИИ -> textContent -> обычный текст на странице
```

<a id="llm06"></a>
## 06. У агента слишком много прав

**Проблема:** задача — прочитать отчёт, но агенту доступны ещё отправка и удаление.

### Уязвимо

```python
allowed_tools = ["read", "send", "delete"]
model_choice = "delete"
tool(model_choice)  # плохо: модель выбрала опасное действие
```

### Защита

```python
user_task = "read_report"
model_choice = "delete"

if user_task == "read_report" and model_choice == "read":
    tool("read")
else:
    print("STOP: это действие не нужно для задачи")
```

```text
Действие ИИ -> if разрешено для задачи -> tool()
                              иначе -> STOP
```

<a id="llm07"></a>
## 07. Секрет спрятан в системном промпте

**Проблема:** ключ положили в текст, который видит модель.

### Уязвимо

```python
system_prompt = "Ты помощник. API_KEY=secret-123"
model(messages=[system_prompt])  # плохо: секрет уже у модели
```

### Защита

```python
system_prompt = "Ты помощник. Кратко объясняй отчёт."
api_key = get_secret_from_server()

if api_key:
    server_call(api_key)  # ключ использует сервер, не модель
else:
    print("STOP: ключ не найден")
```

```text
Секрет -> сервер -> внешний сервис
Промпт -> модель
```

<a id="llm08"></a>
## 08. Поиск нашёл документ другой команды

**Проблема:** поиск по похожести выбирает «подходящий», но чужой документ.

### Уязвимо

```python
all_chunks = ["team-a: отчёт", "team-b: секретный отчёт"]
context = similarity_search(all_chunks, "отчёт")
model(context)  # плохо: поиск не проверил владельца
```

### Защита

```python
user_team = "team-a"
chunks = [
    {"team": "team-a", "text": "отчёт"},
    {"team": "team-b", "text": "секретный отчёт"},
]

allowed_chunks = []
for chunk in chunks:
    if chunk["team"] == user_team:
        allowed_chunks.append(chunk)

context = similarity_search(allowed_chunks, "отчёт")
model(context)
```

```text
Документы -> if команда совпала -> поиск -> ИИ
                         иначе -> не передавать
```

<a id="llm09"></a>
## 09. ИИ уверенно выдумал факт

**Проблема:** ответ звучит убедительно, но источника нет.

### Уязвимо

```python
answer = model("Сколько пользователей?")
print(answer)  # плохо: выводим непроверенный факт
```

### Защита

```python
database = {"users_count": 12}
fact = database.get("users_count")

if fact is not None:
    print("Пользователей:", fact, "Источник: database.users_count")
else:
    print("Нет подтверждённых данных")
```

```text
Вопрос -> if есть источник -> факт + источник
                         иначе -> нет данных
```

<a id="llm10"></a>
## 10. Агент работает бесконечно

**Проблема:** агент повторяет вызов инструмента и тратит лимит.

### Уязвимо

```python
while True:
    tool("search")  # плохо: нет конца и нет бюджета
```

### Защита

```python
max_calls = 3
calls = 0

while calls < max_calls:
    tool("search")
    calls += 1

if calls == max_calls:
    print("STOP: лимит вызовов закончился")
```

```text
Вызов -> if calls < лимит -> tool() -> calls + 1
                         иначе -> STOP
```

---

Это учебные схемы. В реальном приложении проверки доступа, лимиты и секреты должны жить на сервере, а не в ответе ИИ.
