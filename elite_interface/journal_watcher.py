
import os
import json
import time
from pathlib import Path
from .journal_events import event_handlers

journal_dir = Path.home() / "Saved Games/Frontier Developments/Elite Dangerous"
state_file = Path("config/journal_state.json")

def watch_journal(speak_callback):
    log_files = sorted(journal_dir.glob("Journal.*.log"), reverse=True)
    if not log_files:
        print("[Журнал] Файлы журнала не найдены.")
        return

    journal_path = log_files[0]
    print(f"[Журнал] Отслеживание файла: {journal_path}")

    with open(journal_path, "r", encoding="utf-8") as file:
        file.seek(0, os.SEEK_END)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.2)
                continue

            try:
                entry = json.loads(line)
                event = entry.get("event")

                if not event or event not in event_handlers:
                    continue

                if state_file.exists():
                    with open(state_file, "r", encoding="utf-8") as f:
                        state = json.load(f)
                else:
                    state = {}

                event_handlers[event](entry, state, speak_callback)

                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)

            except Exception as e:
                print(f"[Журнал] Ошибка: {e}")
