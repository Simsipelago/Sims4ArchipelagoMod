import json
import os

from lot51_core.utils.paths import get_game_dir
from s4ap.logging.s4ap_logger import S4APLogger

log = S4APLogger.get_log()
log.enable()

GameDir = get_game_dir()
s4ap_directory = os.path.join(GameDir, 'Mods', 'mod_data', 's4ap')
if not os.path.exists(s4ap_directory):
    os.makedirs(s4ap_directory)


def print_json(obj: object, name: str = 'items.json'):
    with open(os.path.join(s4ap_directory, name), 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False)


def read_json(name: str = 'items.json'):
    with open(os.path.join(s4ap_directory, name), 'r', encoding='utf-8') as f:
        d = json.load(f)
    return d
