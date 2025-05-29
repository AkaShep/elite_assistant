import json
from pathlib import Path

def get_item_quantity(item_name: str) -> str:
    elite_dir = Path.home() / "Saved Games/Frontier Developments/Elite Dangerous"
    cargo_path = elite_dir / "Cargo.json"
    locker_path = elite_dir / "ShipLocker.json"

    # Normalize
    query = item_name.lower()

    # Проверяем Cargo
    if cargo_path.exists():
        with open(cargo_path, "r", encoding="utf-8") as f:
            cargo = json.load(f)
            for item in cargo.get("Inventory", []):
                if query in item.get("Name_Localised", "").lower():
                    qty = item.get("Count", 0)
                    return f"У вас {qty} тонн {item.get('Name_Localised')}."

    # Проверяем ShipLocker
    if locker_path.exists():
        with open(locker_path, "r", encoding="utf-8") as f:
            locker = json.load(f)
            for section in ["Components", "Data", "Items", "Consumables"]:
                for item in locker.get(section, []):
                    if query in item.get("Name_Localised", "").lower():
                        qty = item.get("Count", 0)
                        return f"У вас {qty} единиц {item.get('Name_Localised')}."

    return f"Предмет {item_name} не найден в инвентаре."
