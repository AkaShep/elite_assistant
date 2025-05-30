"""
initcopy.py

Модуль выполняет динамическую загрузку команд из текущего каталога.
Он ищет все файлы, оканчивающиеся на _command.py, импортирует их,
создаёт экземпляры командных классов (с именами, оканчивающимися на Command)
и добавляет их в глобальный список commands.

Основные компоненты:
- load_commands: основная функция, отвечающая за загрузку всех команд.

Использование:
from commands import load_commands
load_commands(tts, bindings_loader)
"""

import os
import importlib
from commands.command_dispatcher import CommandDispatcher

def load_commands(tts, bindings_loader):
    """
    Загружает все модули команд из текущей директории, создаёт их экземпляры
    и возвращает список готовых команд.
    """
    commands = []
    commands_dir = os.path.dirname(__file__)

    print(f"[DEBUG] Сканирую директорию команд: {commands_dir}")

    for filename in os.listdir(commands_dir):
        if filename.endswith('_command.py') and filename != '__init__.py':
            module_name = f"{__name__}.{filename[:-3]}"
            print(f"[DEBUG] Загружаю модуль: {module_name}")

            try:
                module = importlib.import_module(module_name)
            except Exception as e:
                print(f"[ERROR] Не удалось импортировать модуль {module_name}: {e}")
                continue

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr_name.endswith('Command'):
                    try:
                        instance = attr(tts, bindings_loader)
                        commands.append(instance)
                        print(f"[DEBUG] Добавлен класс команды: {attr_name}")
                    except Exception as e:
                        print(f"[ERROR] Ошибка создания экземпляра {attr_name} из {module_name}: {e}")

    if not commands:
        print("[WARNING] Не загружено ни одной команды!")

    print("[DEBUG] Загруженные команды:")
    for cmd in commands:
        print(f" - {cmd.__class__.__name__}")

    return commands
