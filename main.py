## main.py
from speech_recognition.recognizer import listen_for_command
from tts_engine.silero_tts import speak, init_tts
import threading
import json
import logging

logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def main():
    print("[Elite Assistant] Запуск...")
    logging.info("[Запуск ассистента]")

    with open("config/settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    init_tts(config)
    load_command_config("config/commands.json")

    journal_thread = threading.Thread(target=watch_journal, args=(speak,), daemon=True)
    journal_thread.start()

    status_thread = threading.Thread(target=watch_status, args=(speak,), daemon=True)
    status_thread.start()

    try:
        while True:
            command = listen_for_command()
            if command:
                logging.info(f"Распознано: {command}")
                print(f"[Команда] Распознано: {command}")
                try:
                    action = interpret_command(command)
                    if action:
                        if "function" in action:
                           if action["function"] == "detect_firegroup_count":
                                detect_firegroup_count(speak)                     
                                continue
                        if "response" in action:
                            speak(action['response'])
                        if "key" in action:
                            press_key(action['key'])
                    else:
                        logging.warning(f"Неизвестная команда: {command}")
                        speak("Команда не распознана")
                except Exception as e:
                    logging.error(f"Ошибка выполнения команды: {e}")
                    speak("Произошла ошибка при выполнении команды")
    except KeyboardInterrupt:
        logging.info("Завершение работы ассистента")
        print("\n[Elite Assistant] Завершение работы.")

if __name__ == "__main__":
    main()