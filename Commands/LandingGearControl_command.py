import keyboard
import requests

class LandingGearControlCommand:
    def __init__(self, tts, bindings_loader, status_client):
        self.tts = tts
        self.bindings_loader = bindings_loader
        self.status_client = status_client
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

        is_landing_gear_down = self.status_client.get_event_value('GearStatusEvent')
        is_in_mothership = self.status_client.get_event_value('InMothershipStatusEvent')


        if not is_in_mothership:
            self.tts.speak("Ты не находишься в корабле. Команда недоступна.")
            return

        keys = self.bindings_loader.get_binding_keys('LandingGearToggle')
        landing_gear_key = '+'.join(keys) if keys else None
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
