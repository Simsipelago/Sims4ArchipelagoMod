import os

from s4ap.logging.s4ap_logger import S4APLogger
from sims4communitylib.utils.common_json_io_utils import CommonJSONIOUtils
from sims4communitylib.utils.common_log_utils import CommonLogUtils

log = S4APLogger.get_log()
log.enable()

ModData = CommonLogUtils.get_mod_data_location_path()
if not os.path.exists(os.path.join(ModData, 's4ap')):
    os.makedirs(os.path.join(ModData, 's4ap'))


def print_json(obj: object, name: str = 'items.json'):
    CommonJSONIOUtils.write_to_file(os.path.join(ModData, 's4ap', name), obj)


def read_json(name: str = 'items.json'):
    d = CommonJSONIOUtils.load_from_file(os.path.join(ModData, 's4ap', name))
    return d
