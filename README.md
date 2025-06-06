# Elite Voice Control Assistant

🛸 **Elite Voice Control Assistant** — голосовой ассистент для управления кораблём в игре *Elite Dangerous* с использованием голосовых команд, EliteAPI и Python.

---

## 📦 Основные возможности

✅ Получение игровых событий через **EliteAPI** (C# REST-сервер)  
✅ Реакция на голосовые команды с помощью **Vosk** (распознавание)  
✅ Голосовые ответы с помощью **Silero TTS**  
✅ управление биндингами с поддержкой комбинаций и раскладок
✅ Нажатие клавиш через биндинги (считанные из игры) с помощью **keyboard**  
✅ Подключение **ShipStatusClient** — общего Python-класса для запросов состояния корабля через REST  
✅ Автоматическая обработка всех вложенных данных из событий EliteAPI  
✅ Гибкая архитектура для расширения: можно быстро писать новые команды и подключать их к ассистенту
✅ общая память ShipMemory
✅ команды на управление шасси
✅ команды на подсчёт и сохранение огневых групп


---

## 🔧 Установка

1️⃣ **Клонируй репозиторий или скачай проект**
```bash
git clone https://github.com/AkaShep/elite_assistant.git
```

2️⃣ Установи зависимости Python:
```bash
pip install -r requirements.txt
```

3️⃣ Собери и запусти REST-сервер (C#):
```bash
cd EliteAPIRestServer
dotnet run
```

4️⃣ Запусти Python-ассистента:
```bash
python main.py
```

---

## 🎙 Голосовые команды

| Категория           | Примеры команд                                   |
|---------------------|--------------------------------------------------|
| Шасси (шасси)       | "выпусти шасси", "убери шасси", "статус шасси"   |
| Огневые группы      | "определи количество огневых групп"              |


---

## ⚙️ Структура проекта

```
elite_assistant/
├── main.py                     # Основной запуск ассистента
├── commands/                   # Папка с командами
├── utils/                      # Вспомогательные модули (TTS, bindings, ShipStatusClient)
├── recognizer.py               # Модуль распознавания голоса
EliteAPIRestServer/             # C# REST-сервер с EliteAPI
```

---

## 💡 Особенности

✨ Используется fuzzy matching для гибкого сопоставления команд  
✨ ShipStatusClient централизует работу с REST API  
✨ Поддержка вложенных данных из всех событий (с автоматической распаковкой)  
✨ Можно быстро добавлять свои команды по готовому шаблону  
✨ Работает локально, без отправки данных в интернет

---

## 📞 Поддержка

Если нужны доработки или помощь — пиши!
