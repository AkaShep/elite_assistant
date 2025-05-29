import json
import time
from utils.hotkey_emulator import press_key


number_words = {
    "ноль": 0, "один": 1, "одна": 1, "два": 2, "две": 2, "три": 3,
    "четыре": 4, "пять": 5, "шесть": 6, "семь": 7, "восемь": 8,
    "девять": 9, "десять": 10
}

def detect_firegroup_count(speak):
    seen = set()
    max_attempts = 10
    key = "n"
    last_value = None

    speak("Начинаю определение огневых групп")

    for _ in range(max_attempts):
        press_key(key)
        time.sleep(0.8)

        try:
            with open("config/state.json", "r", encoding="utf-8") as f:
                state = json.load(f)
            current = state.get("FireGroup")
            if current is None:
                continue
            if last_value is None:
                last_value = current
            if current in seen and len(seen) > 1:
                break
            seen.add(current)
        except Exception as e:
            print(f"[Ошибка определения групп]: {e}")

    count = len(seen)
    try:
        with open("config/state.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        state["FireGroupCount"] = count
        with open("config/state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[Ошибка записи количества групп]: {e}")

    speak(f"У вас {count} огневых групп")


def switch_firegroup(speak):
    try:
        with open("config/state.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        target = int(input("Введите номер огневой группы (начиная с 1): ")) - 1
        current = state.get("FireGroup", 0)
        total = state.get("FireGroupCount", 0)
        if total <= 1 or target == current:
            speak("Переключение не требуется")
            return
        forward = (target - current) % total
        backward = (current - target) % total
        if forward <= backward:
            for _ in range(forward):
                press_key("n")
                time.sleep(1)
        else:
            for _ in range(backward):
                press_key("shift+n")
                time.sleep(1)
        time.sleep(1)
        with open("config/state.json", "r", encoding="utf-8") as f:
            new_state = json.load(f)
        if new_state.get("FireGroup") == target:
            speak(f"Огневая группа {target + 1} активна")
        else:
            speak("Не удалось переключить огневую группу")
    except Exception as e:
        speak(f"Ошибка: {e}")

import re

def switch_firegroup_direct(command, speak):
    try:
        command = command.lower()
        match = re.search(r"(огневая группа|переключи на группу)\s*(\d+)", command)
        if match:
            target = int(match.group(2)) - 1
        else:
            for word, num in number_words.items():
                if word in command:
                    target = num - 1
                    break
            else:
                speak("Не указана огневая группа")
                return
        target = int(match.group(2)) - 1
        with open("config/state.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        current = state.get("FireGroup", 0)
        total = state.get("FireGroupCount", 0)
        if total <= 1 or target == current:
            speak("Переключение не требуется")
            return
        forward = (target - current) % total
        backward = (current - target) % total
        if forward <= backward:
            for _ in range(forward):
                press_key("n")
                time.sleep(1)
        else:
            for _ in range(backward):
                press_key("shift+n")
                time.sleep(1)
        time.sleep(1)
        with open("config/state.json", "r", encoding="utf-8") as f:
            new_state = json.load(f)
        if new_state.get("FireGroup") == target:
            speak(f"Огневая группа {target + 1} активна")
        else:
            speak("Не удалось переключить огневую группу")
    except Exception as e:
        speak(f"Ошибка: {e}")

