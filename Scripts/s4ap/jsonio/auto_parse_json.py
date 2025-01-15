import os

from s4ap.enums import ap_cmds
from s4ap.events.Utils.allow_read_items import AllowReceiveItems
from s4ap.events.items.receive_item_event import ReceiveItemEvent
from s4ap.jsonio.s4ap_json import read_json, print_json
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.interval.common_interval_event_service import CommonIntervalEventRegistry
from sims4communitylib.events.save.events.save_loaded import S4CLSaveLoadedEvent
from sims4communitylib.utils.common_log_utils import CommonLogUtils

logger = S4APLogger.get_log()
logger.enable()

Toggle = False
old_data = None
old_mtime = None
cancel = True
files = ['connection_status.json',
         'items.json']
file_data = {}


def get_path(name: str):
    return os.path.join(CommonLogUtils.get_mod_data_location_path(), 's4ap', name)


class DetectGameStatus:

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity().name)
    def _on_save_loaded(event_data: S4CLSaveLoadedEvent):
        global file_data
        global cancel
        for file in files:
            file_data[file] = {}
        cancel = True
        logger.debug('save loaded')


@CommonIntervalEventRegistry.run_every(ModInfo.get_identity().name, milliseconds=500)
def auto_read_data():
    global file_data
    for file in files:  # iterates through the list of files
        if file not in file_data:  # if the file is not in found in file_data
            file_data[file] = {}  # defines it as blank to file_data
        f = file_data[file]  # 'f' is acting as file_data[file], changes to f will change file_data[file]
        if os.path.exists(get_path(file)):
            new_mtime = os.path.getmtime(get_path(file))
            if new_mtime != f.get("mtime"):  # if the time of modification of the file is different
                # to the defined modification time (e.g. edited more recently)
                f["mtime"] = new_mtime  # then set it to the new one
                new_data = read_json(file)
                if isinstance(new_data, dict) and new_data != f.get(
                        "data"):  # if the new data is different to the defined data
                    f["data"] = new_data  # then set it to the new data
                    if new_data:
                        parse_message(new_data)
        else:
            print_json(None, file)


def parse_message(data):
    global cancel
    cmd = data["cmd"]
    if cmd == ap_cmds.CONNECTED:
        # Check if connection data already exists in storage for save and is the same
        logger.debug("cmd CONNECTED received")
        host = data["host"]
        port = data["port"]
        seed_name = data["seed_name"]
        slot_name = data["name"]
        goal = data["goal"]
        career = data["career"]
        data_store = S4APSessionStoreUtils()
        data_store.save_goal_and_career(goal, career)
        if data_store.check_session_values(host_name=host, port=port, seed_name=seed_name,
                                           player=slot_name):
            # if settings don't match then cancels
            cancel = True
            print_json({})

        else:
            cancel = False  # if values match then don't cancel
    elif not cancel:
        if cmd == ap_cmds.RECEIVEDITEMS:
            logger.debug("cmd RECEIVEDITEMS received")
            # [{"cmd":"ReceivedItems","index":0,"items":[{"item":80000,"location":-1,"player":0,"flags":0,"class":"NetworkItem"}]}]
            index = data["index"]
            items = data["items"]
            item_ids = data["item_ids"]
            locations = data["locations"]
            players = data["players"]
            CommonEventRegistry.get().dispatch(
                ReceiveItemEvent(index=index, items=items, item_ids=item_ids, locations=locations, players=players))
        else:
            logger.debug(f"cmd {cmd} received")
            logger.debug(f"Unhandled message received: {str(data)}")
    else:
        logger.debug('cancel is true')


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_allow_receive_items(event_data: AllowReceiveItems):
    global cancel
    global file_data
    cancel = not event_data.is_allowed
    print_json(True, 'sync.json')
    for file in files:
        file_data[file] = {}
