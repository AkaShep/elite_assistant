# utils/hotkey_emulator.py
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def press_key(key):
    print(f"[PRESS] Key: {key}")
    if '+' in key:
        parts = key.split('+')
        with keyboard.pressed(getattr(Key, parts[0])):
            keyboard.press(parts[1])
            keyboard.release(parts[1])
    else:
        keyboard.press(key)
        time.sleep(0.05)
        keyboard.release(key)


