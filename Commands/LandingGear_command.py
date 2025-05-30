import requests

class LandingGearCommand:
    def __init__(self, tts, bindings_loader):
        self.tts = tts    # Silero TTS экземпляр
        self.bindings_loader = bindings_loader 
        self.priority = 20
        self.match_threshold = 60
        self.last_recognized_command = ""
        self.test_phrases = [
            "статус шасси",
            ] 
      

    def execute(self):
        self.tts.speak("Проверяю статус шасси...")
        try:
            response = requests.get('http://localhost:5000/ship-status')
            response.raise_for_status()
            data = response.json()
            is_landing_gear_down = data.get('isLandingGearDown')

            if is_landing_gear_down is None:
                self.tts.speak("Не удалось получить статус шасси.")
            elif is_landing_gear_down:
                self.tts.speak("Шасси выпущены!")
            else:
                self.tts.speak("Шасси скрыты!")
        except Exception as e:
            print(f"Ошибка: {e}")
            self.tts.speak("Произошла ошибка при запросе к серверу.")
