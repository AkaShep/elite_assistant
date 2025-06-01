## main.py
from speech_recognition.recognizer import Recognizer
from tts_engine.silero_tts import speak, init_tts
from commands import load_commands, CommandDispatcher
import threading
import queue
import json
import logging
import time
from utils.bindings_loader import BindingsLoader
from utils.ship_status_client import ShipStatusClient
from utils.ship_memory import ShipMemory

logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Очередь для передачи текста в TTS
tts_queue = queue.Queue()

# Обёртка с методом speak для совместимости с командами
class TTSWrapper:
    def speak(self, text):
        print(f"[TTS] {text}")
        tts_queue.put(text)

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        speak(text)
        tts_queue.task_done()

def combat_mode_checker(status_client, tts_wrapper):
    previous_combat_mode = None
    while True:
        try:
            in_combat = status_client.get_event_value("InDangerStatusEvent", "Value")
            if in_combat != previous_combat_mode:
                previous_combat_mode = in_combat
                if in_combat:
                    tts_wrapper.speak("Боевой режим активирован. Переходим на прямое управление.")
                else:
                    tts_wrapper.speak("Штатный режим активен. Ожидаю ключевое слово.")
        except Exception as e:
            print(f"[CombatModeChecker] Ошибка при проверке режима: {e}")
        time.sleep(1)  # раз в секунду проверка        

def main():
    print("[Elite Assistant] Запуск...")
    logging.info("[Запуск ассистента]")

    with open("config/settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    init_tts(config)

    # Инициализация обёртки и биндингов
    
    recognizer = Recognizer()
    tts_wrapper = TTSWrapper()
    bindings_loader = BindingsLoader()
    bindings_loader.load_bindings()
    status_client = ShipStatusClient()
    memory = ShipMemory()

    # Загружаем команды и диспетчер
    all_commands = load_commands(tts_wrapper, bindings_loader, status_client, memory)
    dispatcher = CommandDispatcher(all_commands, threshold=70)

    if all_commands:
        print("[DEBUG] Загружены команды:")
        for command in all_commands:
            print(f"[DEBUG] -> {command.__class__.__name__}")
            if hasattr(command, 'test_phrases'):
                print(f"[DEBUG] Тестовые фразы для {command.__class__.__name__}: {command.test_phrases}")
    else:
        print("[WARNING] Команды не загружены!")

    # Запуск TTS потока
    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    tts_thread.start()

    combat_thread = threading.Thread(target=combat_mode_checker, args=(status_client, tts_wrapper), daemon=True)
    combat_thread.start()

    # Слежение за сменой боевого режима
    previous_combat_mode = None

    try:
        while True:

            # Проверяем команды
            recognized_text = recognizer.listen_for_command()
            if recognized_text:
                recognized_text = recognized_text.lower().strip()
                print(f"Распознано: '{recognized_text}'")
                handled = dispatcher.handle(recognized_text)
                print(f"[DEBUG] dispatcher.handle вернул: {handled}")
                if not handled:
                    tts_queue.put("Команда не распознана.")
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка во время выполнения: {e}")
    finally:
        tts_queue.put(None)
        tts_thread.join()

if __name__ == "__main__":
    main()
