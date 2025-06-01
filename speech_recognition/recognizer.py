# speech_recognition/recognizer.py
import vosk
import sys
import sounddevice as sd
import queue
import json
from rapidfuzz import fuzz
from utils.ship_status_client import ShipStatusClient

q = queue.Queue()
model = vosk.Model(lang="ru")


class Recognizer:
    def __init__(self):
        self.wake_word = ["гидеон", "гидон", "гидэон", "кидо", "гиды он", "кеды он", "кидман", "кидо он", "да он"]
        self.model = model
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.ship_status = ShipStatusClient()
        self.previous_combat_mode = None  # последнее известное состояние

    def callback(self,indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(bytes(indata))    

    def listen_for_command(self):
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=self.callback):
            print("[Recognizer] Начинаю слушать...")
            while True:
                data = q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    if not text:
                        continue

                    in_combat = self.ship_status.get_event_value("InDangerStatusEvent", "Value")
                    print(f"[Recognizer] Распознано: '{text}' (combat={in_combat})")

                    if in_combat:
                        return text
                    else:
                        for word in self.wake_word:
                            similarity = fuzz.partial_ratio(word, text)
                            if similarity >= 80:
                                print("[Recognizer] Wake word активировано!")
                                cleaned = text.replace(word, "").strip()
                                if cleaned:
                                    return cleaned
                                else:
                                    print("[Recognizer] Жду команды после ключевого слова...")

    def check_combat_mode_change(self):
        """Проверяет, сменился ли боевой режим. Возвращает True/False при смене, иначе None."""
        try:
            in_combat = self.ship_status.get_event_value("InDangerStatusEvent", "Value")
            if in_combat != self.previous_combat_mode:
                self.previous_combat_mode = in_combat
                return in_combat  # режим изменился → возвращаем новый
        except Exception as e:
            print(f"[Recognizer] Ошибка при проверке боевого режима: {e}")
        return None