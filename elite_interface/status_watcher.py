import os
import json
import time
from pathlib import Path

def watch_status(speak_callback):
    path = Path.home() / "Saved Games/Frontier Developments/Elite Dangerous/Status.json"
    modules_path = Path.home() / "Saved Games/Frontier Developments/Elite Dangerous/ModulesInfo.json"
    state_path = Path("config/state.json")
    flags_path = Path("config/flags.json")

    if not path.exists() or not flags_path.exists():
        print("[Статус] Отсутствует Status.json или flags.json.")
        return

    while True:
        try:
            with open(path, "r", encoding="utf-8") as f:
                current = json.load(f)
            flags = current.get("Flags", 0)

            with open(flags_path, "r", encoding="utf-8") as fp:
                flag_definitions = json.load(fp)
            status_bits = {name: bool(flags & bit) for name, bit in flag_definitions.items()}

            # Добавляем параметры из Status.json
            for key in ["Pips", "FireGroup", "GuiFocus", "Cargo", "Balance"]:
                if key in current:
                    status_bits[key] = current[key]

            if "Fuel" in current:
                fuel = current["Fuel"]
                status_bits["FuelMain"] = fuel.get("FuelMain", 0)
                status_bits["FuelReservoir"] = fuel.get("FuelReservoir", 0)

                with open(state_path, "w", encoding="utf-8") as sf:
                    json.dump(status_bits, sf, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"[Статус] Ошибка: {e}")

        time.sleep(0.5)
