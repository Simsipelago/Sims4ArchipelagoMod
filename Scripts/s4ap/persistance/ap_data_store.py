from typing import Any, Dict

from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore


class S4APSettings:
    MOD_VERSION = 'mod_version'  # Fixed at time of first start
    SEED_NAME = 'seed_name'  # From RoomInfo and if set checked against it to prevent booting of multiple seeds per save
    HOST_NAME = 'host'  # From Login and if set checked against it to prevent booting of multiple seeds per save
    PORT_NUMBER = 'port'  # From Login and if set checked against it to prevent booting of multiple seeds per save
    PLAYER = 'player'  # From RoomInfo and if set checked against it to prevent booting of multiple seeds per save
    INDEX = 'index'  # Index received from ReceivedItems
    ITEMS = 'items'  # Items received from ReceivedItems
    ITEM_IDS = 'item_ids'  # Item ids received from ReceivedItems
    LOCATIONS = 'locations'  # The Locations for the received items in ReceivedItems
    SENDERS = 'senders'  # The players who sent the item
    GOAL = 'goal' # the goal of the game
    CAREER = 'career' # the chosen career for logic
    SLOT = 'slot' # From RoomInfo and if set checked to ensure bleeding doesn't happen (the slot number of the slot)

class S4APGenericDataStore(CommonDataStore):
    """ Manager of generic stuff. """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_identifier(cls) -> str:
        return 's4ap_generic_settings'

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _version(self) -> int:
        # We specify a version so that when the data set changes we can force an update of the data set within the game of players.
        return 1

    # noinspection PyMissingOrEmptyDocstring
    @property
    def _default_data(self) -> Dict[str, Any]:
        # We specify the default values for our data within here.
        return {
            S4APSettings.MOD_VERSION: self._version,
            S4APSettings.SEED_NAME: None,
            S4APSettings.HOST_NAME: "archipelago.gg", # this should be a string
            S4APSettings.PORT_NUMBER: 38281, # this should be an integer
            S4APSettings.PLAYER: None, # this should be a string
            S4APSettings.INDEX: None, # this should be an integer
            S4APSettings.ITEMS: None, # this should be a List[str] (a list of strings)
            S4APSettings.ITEM_IDS: None, # this should be a List[int] (a list of integers)
            S4APSettings.LOCATIONS: None, # this should be a List[str] (a list of strings)
            S4APSettings.SENDERS: None, # this should be a List[str] (a list of strings)
            S4APSettings.GOAL: None, # this should be a string
            S4APSettings.CAREER: None, # currently this is a string, but in future versions, it will be a set coming from AP, which will probably deserialize as a list? i don't know exactly how JSON deserialization works with S4CL. from poking around, it'll be a list of strings, so it's been adjusted accordingly.
            S4APSettings.SLOT: 1, # this should be an integer, if it isn't, something has gone terribly wrong here
        }.copy()
