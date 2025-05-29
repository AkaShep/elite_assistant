# command_parser/parser.py
import json
from pathlib import Path

commands = []

def load_command_config(path):
    global commands
    with open(path, "r", encoding="utf-8") as f:
        commands = json.load(f)

def interpret_command(command):
    command = command.lower()
    for item in commands:
        if any(phrase in command for phrase in item["phrases"]):
            result = {}
            if "key" in item:
                result["key"] = item["key"]
            if "response" in item:
                result["response"] = item["response"]
            if "function" in item:
                result["function"] = item["function"]
            return result
    return None
