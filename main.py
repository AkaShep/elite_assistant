## main.py
from speech_recognition.recognizer import listen_for_command
from tts_engine.silero_tts import speak, init_tts
from commands import load_commands, CommandDispatcher
import threading
import queue
import json
import logging
from utils.bindings_loader import BindingsLoader
from utils.ship_status_client import ShipStatusClient

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

def main():
    print("[Elite Assistant] Запуск...")
    logging.info("[Запуск ассистента]")

    with open("config/settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    init_tts(config)

    # Инициализация обёртки и биндингов
    tts_wrapper = TTSWrapper()
    bindings_loader = BindingsLoader()
    bindings_loader.load_bindings()
    status_client = ShipStatusClient()

    # Загружаем команды и диспетчер
    all_commands = load_commands(tts_wrapper, bindings_loader, status_client)
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

    try:
        while True:
            recognized_text = listen_for_command()
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
