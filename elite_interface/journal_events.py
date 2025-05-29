
def handle_jump(entry, state, speak_callback):
    system = entry.get("StarSystem", "неизвестная система")
    state["last_jump"] = system
    speak_callback(f"Прыжок в систему {system}")

def handle_attack(entry, state, speak_callback):
    state["under_attack"] = True
    speak_callback("Вы под атакой")

def handle_docking(entry, state, speak_callback):
    station = entry.get("StationName")
    state["last_docking"] = station
    speak_callback(f"Посадка разрешена на станции {station}")

def handle_loadout(entry, state, speak_callback):
    ship = entry.get("Ship")
    state["last_ship"] = ship

event_handlers = {
    "FSDJump": handle_jump,
    "UnderAttack": handle_attack,
    "DockingGranted": handle_docking,
    "Loadout": handle_loadout,
}
