import requests
import keyboard

class BindingsLoader:
    russian_to_latin = {
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i',
        'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's', 'в': 'd', 'а': 'f',
        'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'ж': ';', 'э': "'", 'я': 'z',
        'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.',
        'ё': '`'
    }

    def __init__(self, server_url='http://localhost:5000'):
        self.server_url = server_url
        self.bindings = {}

    def load_bindings(self):
        try:
            response = requests.get(f'{self.server_url}/bindings')
            response.raise_for_status()
            self.bindings = response.json()
            print(f"[BindingsLoader] Загружено {len(self.bindings)} биндингов")
        except Exception as e:
            print(f"[BindingsLoader] Ошибка при загрузке биндингов: {e}")
            self.bindings = {}

    def get_binding_keys(self, binding_name):
        key_str = self.bindings.get(binding_name)
        if not key_str or key_str == 'not set':
            print(f"[BindingsLoader] Биндинг '{binding_name}' не найден или не назначен")
            return None

        keys = [self.clean_key_name(k) for k in key_str.split('+')]
        return keys

    def press_binding(self, binding_name):
        keys = self.get_binding_keys(binding_name)
        if not keys:
            print(f"[BindingsLoader] Не могу прожать биндинг '{binding_name}'")
            return

        combo = '+'.join(keys)
        print(f"[BindingsLoader] Нажимаю: {combo}")
        keyboard.press_and_release(combo)

    @classmethod
    def clean_key_name(cls, key_name):
        if key_name.startswith('Key_'):
            key = key_name[4:].lower()
            if key in cls.russian_to_latin:
                return cls.russian_to_latin[key]
            return key
        return key_name.lower()
