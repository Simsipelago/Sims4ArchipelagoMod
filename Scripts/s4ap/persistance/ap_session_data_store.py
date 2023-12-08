from typing import Any

from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.persistance.ap_data_store import S4APSettings, S4APGenericDataStore
from s4ap.persistance.ap_data_utils import S4APDataManagerUtils
from s4ap.utils.s4ap_generic_utils import S4APUtils

logger = S4APLogger.get_log()
logger.enable()


class S4APSessionStoreUtils:
    """ Session Setting Utilities. """
    def __init__(self) -> None:
        self._data_manager = S4APDataManagerUtils()

    def check_session_values(self, host_name: str, port: str, seed_name: str, player: str) -> bool:
        """ Check session store to make sure it's the same settings as before and send a warning otherwise
            :returns True, if settings don't exist or equal those that were used before """
        if self._get_value(S4APSettings.SEED_NAME) is not None:  # Check if Seed was previously saved
            logger.debug("Seed found")
            if self._get_value(S4APSettings.SEED_NAME) != seed_name or \
                    self._get_value(S4APSettings.HOST_NAME) != host_name or \
                    self._get_value(S4APSettings.PORT_NUMBER) != port or \
                    self._get_value(S4APSettings.PLAYER) != player:  # Settings don't match
                logger.warn("AP connection setting mismatch")
                return False
            else:  # Settings exist and match
                logger.debug("Settings matched")
                return True
        else:
            logger.debug("Storing initial AP data")
            self.save_seed_values(host_name, port, seed_name, player)  # Store data initially
            return True

    def check_datapackage_version(self, package_version: int) -> bool:
        """ Check session store to make sure the Datapackage version hasn't changed
            :returns True, if Datapackage version is 0 or matches """
        current_version= self._get_value(S4APSettings.RECEIVED_DATAPACKAGE_VERSION)
        if package_version == 0 or current_version == 0 or \
                current_version == package_version:
            if current_version == 0 and package_version != 0:  # Store package version if it was 0 previously
                self._set_value(S4APSettings.RECEIVED_DATAPACKAGE_VERSION, package_version)
                S4APUtils.trigger_autosave()
            return True
        else:
            return False

    def save_seed_values(self, host_name: str, port: str, seed_name: str, player: str):
        """ Overwrite Session specific values. """
        self._set_value(S4APSettings.SEED_NAME, seed_name)
        self._set_value(S4APSettings.HOST_NAME, host_name)
        self._set_value(S4APSettings.PORT_NUMBER, port)
        self._set_value(S4APSettings.PLAYER, player)
        S4APUtils.trigger_autosave()

    def _get_value(self, key: str) -> Any:
        generic_settings_data_store: S4APGenericDataStore = self._data_manager.get_generic_settings_data()
        return generic_settings_data_store.get_value_by_key(key)

    def _set_value(self, key: str, value: Any):
        generic_settings_data_store: S4APGenericDataStore = self._data_manager.get_generic_settings_data()
        return generic_settings_data_store.set_value_by_key(key, value)
