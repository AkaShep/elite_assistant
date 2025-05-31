import requests

class ShipStatusClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url

    def get_status(self):
        try:
            response = requests.get(f'{self.base_url}/ship-status')
            response.raise_for_status()
            data = response.json()
            events = data.get('events') or {}
            return events
        except Exception as e:
            print(f"[ShipStatusClient ERROR] {e}")
            return None

    def get_event_value(self, event_name, field='Value'):
        events = self.get_status()
        if not events:
            return None
        return events.get(event_name, {}).get(field)
