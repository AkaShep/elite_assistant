import keyboard
import requests

class LandingGearControlCommand:
    def __init__(self, tts, bindings_loader):
        self.tts = tts
        self.bindings_loader = bindings_loader
        self.priority = 20
        self.match_threshold = 60
        self.last_recognized_command = ""
        self.test_phrases = [
            "выпусти шасси",
            "опусти шасси",
            "выпустить шасси",
            "открой шасси",
            "убери шасси",
            "подними шасси"
        ]

    def execute(self):
        # Определяем действие на основе последних слов
        action_word = None
        for word in self.last_recognized_command.split():
            if word in ["выпусти", "выпустить", "опусти", "открой"]:
                action_word = "опустить"
            elif word in ["убери", "подними", "убрать"]:
                action_word = "убрать"

        if not action_word:
            self.tts.speak("Не удалось понять, что делать с шасси.")
            return

        try:
            response = requests.get('http://localhost:5000/ship-status')
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка при запросе к серверу: {e}")
            self.tts.speak("Ошибка получения состояния корабля.")
            return

        is_landing_gear_down = data.get('isLandingGearDown')
        is_in_mothership = data.get('inMothershipStatus')

        if not is_in_mothership:
            self.tts.speak("Ты не находишься в корабле. Команда недоступна.")
            return

        landing_gear_key = self.bindings_loader.get_binding_key('LandingGearToggle')
        if not landing_gear_key:
            self.tts.speak("Не удалось найти клавишу для управления шасси.")
            return

        if action_word == "опустить":
            if not is_landing_gear_down:
                self.tts.speak("Выпускаю шасси.")
                keyboard.press_and_release(landing_gear_key)
            else:
                self.tts.speak("Шасси уже выпущены.")
        elif action_word == "убрать":
            if is_landing_gear_down:
                self.tts.speak("Убираю шасси.")
                keyboard.press_and_release(landing_gear_key)
            else:
                self.tts.speak("Шасси уже убраны.")
        else:
            self.tts.speak("Неизвестное действие для шасси.")
