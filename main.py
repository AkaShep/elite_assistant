## main.py
from speech_recognition.recognizer import listen_for_command
from tts_engine.silero_tts import speak, init_tts
import threading
import queue
import json
import logging

logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Очередь для передачи текста в TTS
tts_queue = queue.Queue()

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break  # Выход из потока при получении None
        speak(text)
        tts_queue.task_done()

def main():
    print("[Elite Assistant] Запуск...")
    logging.info("[Запуск ассистента]")

    with open("config/settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    init_tts(config)

    # Запуск TTS потока
    tts_thread = threading.Thread(target=tts_worker, daemon=True)
    tts_thread.start()

    try:
        while True:
            recognized_text = listen_for_command()
            if recognized_text:
                print(f"Распознано: {recognized_text}")
                tts_queue.put(recognized_text)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка во время выполнения: {e}")
    finally:
        # Завершаем поток TTS
        tts_queue.put(None)
        tts_thread.join()

if __name__ == "__main__":
    main()
