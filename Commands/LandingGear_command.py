import requests

class LandingGearCommand:
    def __init__(self, tts, bindings_loader, status_client, memory):
        self.tts = tts    # Silero TTS экземпляр
        self.bindings_loader = bindings_loader 
        self.status_client = status_client
        self.priority = 20
        self.match_threshold = 60
        self.last_recognized_command = ""
        self.test_phrases = [
            "статус шасси",
            ] 
      

    def execute(self):
        self.tts.speak("Проверяю статус шасси...")
        try:
            is_landing_gear_down = self.status_client.get_event_value('GearStatusEvent')

            if is_landing_gear_down is None:
                self.tts.speak("Не удалось получить статус шасси.")
            elif is_landing_gear_down:
                self.tts.speak("Шасси выпущены!")
            else:
                self.tts.speak("Шасси скрыты!")
        except Exception as e:
            print(f"Ошибка: {e}")
            self.tts.speak("Произошла ошибка при запросе к серверу.")

