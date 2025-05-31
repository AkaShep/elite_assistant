import time
import keyboard

class ShipFireGroupCounterCommand:
    def __init__(self, tts, bindings_loader, status_client, memory):
        self.tts = tts
        self.bindings_loader = bindings_loader
        self.status_client = status_client
        self.firegroup_binding = 'CycleFireGroupNext'
        self.memory = memory
        self.test_phrases = [
            "определи количество огневых групп",
            ] 

    def get_current_firegroup(self):
        try:
            status = self.status_client.get_status()
            current = status['StatusEvent']['FireGroup']
            return current
        except Exception as e:
            print(f"[FireGroupCounter] Ошибка чтения статуса: {e}")
            return None

    def execute(self):
        self.tts.speak("Определяю количество огневых групп...")
        print("[FireGroupCounter] Старт подсчёта")

        initial_group = self.get_current_firegroup()
        if initial_group is None:
            self.tts.speak("Не удалось получить текущий огневой слот.")
            return

        seen_groups = set()
        count = 0

        while True:
            current_group = self.get_current_firegroup()
            if current_group is None:
                self.tts.speak("Ошибка чтения огневого слота.")
                return

            if current_group in seen_groups:
                # Мы вернулись на первый найденный → круг замкнулся
                break

            seen_groups.add(current_group)
            count += 1

            print(f"[FireGroupCounter] Слот {current_group}, всего найдено: {count}")
            keys = self.bindings_loader.get_binding_keys(self.firegroup_binding)
            if not keys:
                self.tts.speak("Не удалось найти биндинг для переключения огневых групп.")
                return

            keyboard.press_and_release('+'.join(keys))
            time.sleep(2)  # даём серверу время обновить статус
            
        self.memory.set('fire_group_count', count)
        self.tts.speak(f"На корабле настроено {count} огневых групп.")
        print(f"[FireGroupCounter] Всего огневых групп: {count}")
