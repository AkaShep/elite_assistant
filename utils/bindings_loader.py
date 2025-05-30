import requests

class BindingsLoader:
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

    def get_binding_key(self, binding_name):
        key = self.bindings.get(binding_name)
        if not key or key == 'not set':
            print(f"[BindingsLoader] Биндинг '{binding_name}' не найден или не назначен")
            return None
        return self.clean_key_name(key)

    @staticmethod
    def clean_key_name(key_name):
        if key_name.startswith('Key_'):
            return key_name[4:].lower()
        return key_name.lower()
