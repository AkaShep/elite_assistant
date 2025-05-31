import json
import os

class ShipMemory:
    def __init__(self, filename='ship_memory.json'):
        self.filename = filename
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def clear(self):
        self.data = {}
        self._save()
