"""
command_dispatcher.py

Модуль содержит класс CommandDispatcher, который отвечает за обработку
входных текстовых команд и их сопоставление с зарегистрированными командами
на основе метрик схожести (с помощью библиотеки rapidfuzz).

Основные компоненты:
- CommandDispatcher: перебирает список команд, сравнивает входной текст с test_phrases каждой команды,
  и если схожесть превышает порог threshold, запускает соответствующую команду.

Использование:
dispatcher = CommandDispatcher(commands)
dispatcher.handle("поднять шасси")
"""

from rapidfuzz import fuzz

class CommandDispatcher:
    def __init__(self, commands, threshold=70):
        """
        Инициализация диспетчера команд.

        :param commands: список объектов команд, каждая должна иметь атрибут test_phrases (список строк)
        :param threshold: минимальный порог схожести (0-100) для активации команды
        """
        self.commands = commands
        self.threshold = threshold

    def handle(self, text):
        """
        Обрабатывает входной текст, проверяя его на схожесть с test_phrases каждой команды.

        :param text: входная строка (например, команда, распознанная из речи)
        :return: True, если была активирована хотя бы одна команда, иначе False
        """
        if len(text.strip()) < 3:
                    print("[DISPATCHER DEBUG] Введён слишком короткий текст, пропускаем.")
                    return False

        best_command = None
        best_score = 0
        best_priority = -1
        best_phrase = ""

        matched = False
        for command in self.commands:
            threshold = getattr(command, 'match_threshold', 60)
            priority = getattr(command, 'priority', 10)
            for phrase in getattr(command, 'test_phrases', []):
                score = fuzz.partial_ratio(text, phrase)
                print(f"[DISPATCHER DEBUG] '{text}' ↔ '{phrase}' = {score}")
                if score >= threshold:
                    if (score > best_score) or (score == best_score and priority > best_priority):
                        best_score = score
                        best_command = command
                        best_priority = priority
                        best_phrase = phrase

        if best_command:
            print(f"[DISPATCHER DEBUG] ЛУЧШЕЕ СОВПАДЕНИЕ: {best_phrase} (score={best_score}) → {best_command.__class__.__name__}")
            best_command.last_recognized_command = text
            best_command.execute()
            return True
        return matched
