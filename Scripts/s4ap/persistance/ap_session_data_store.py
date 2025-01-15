from typing import Any
from s4ap.jsonio.s4ap_json import print_json
from s4ap.events.Utils.allow_read_items import AllowReceiveItems
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.persistance.ap_data_store import S4APGenericDataStore, S4APSettings
from s4ap.persistance.ap_data_utils import S4APDataManagerUtils
from s4ap.utils.s4ap_generic_utils import S4APUtils
from s4ap.utils.s4ap_reset_utils import ResetSimData
from sims4communitylib.dialogs.ok_cancel_dialog import CommonOkCancelDialog
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.localization.common_localized_string_colors import CommonLocalizedStringColor
from ui.ui_dialog import UiDialogOkCancel

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
                logger.warn("AP session data mismatch")

                def _cancel_chosen(_: UiDialogOkCancel):
                    # If cancel is chosen, stop parsing data until connection_status.json changes
                    return True

                def _ok_chosen(_: UiDialogOkCancel):
                    logger.debug("Ok Chosen, Saving data...")
                    reset = ResetSimData()
                    reset.reset_all_skills()
                    reset.remove_all_s4ap_traits()
                    reset.show_reset_notif()
                    S4APDataManagerUtils.get().reset()
                    self.save_seed_values(host_name, port, seed_name, player)
                    print_json({}, 'items.json')
                    print_json(True, 'sync.json')
                    print_json({}, 'locations_cached.json')
                    CommonEventRegistry.get().dispatch(AllowReceiveItems(True))
                    return False  # if okay is chosen then save seed values and resync items

                # Prompt the user to either overwrite the previous session_data, or stop parsing the data packet and wait for the connection_status.json to update
                dialog = CommonOkCancelDialog(
                    CommonLocalizationUtils.create_localized_string('Warning!',
                                                                    text_color=CommonLocalizedStringColor.RED),
                    description_identifier="There's a mismatch with your AP session data. If you press 'Overwrite,' all previous items will be resynced, and your Sims' skill levels will reset. If you'd rather keep your current progress, select 'Cancel' and switch to a different save file so you can come back to this session later.",
                    ok_text_identifier='Overwrite'
                )
                dialog.show(on_ok_selected=_ok_chosen, on_cancel_selected=_cancel_chosen)
                return True
            else:  # Settings exist and match
                logger.debug("AP session data matched")
                return False
        else:
            logger.debug("Storing initial AP session data")

            def _ok_chosen(_: UiDialogOkCancel):
                logger.debug("Ok Chosen, Saving data...")
                reset = ResetSimData()
                reset.reset_all_skills()
                reset.remove_all_s4ap_traits()
                reset.show_reset_notif()
                print_json({}, 'items.json')
                print_json(True, 'sync.json')
                print_json({}, 'locations_cached.json')
                CommonEventRegistry.get().dispatch(AllowReceiveItems(True))
                self.save_seed_values(host_name, port, seed_name, player)
                return False

            def _cancel_chosen(_: UiDialogOkCancel):
                return True

            # Prompt the user to either overwrite the previous session_data, or stop parsing the data packet and wait for the connection_status.json to update
            dialog = CommonOkCancelDialog(
                CommonLocalizationUtils.create_localized_string('Warning!',
                                                                text_color=CommonLocalizedStringColor.RED),
                description_identifier="Pressing 'Connect' will reset your Sims' skill levels and will sync the game to the client. If you don't want to use this save, click 'Cancel' and switch to a different one.",
                ok_text_identifier='Connect'
            )
            dialog.show(on_ok_selected=_ok_chosen, on_cancel_selected=_cancel_chosen)
            return True

    def check_index_value(self, index: str) -> bool:
        """Checks The Index from ReceivedItems to make sure it matches
            :returns True, if Index matches or if it's zero"""
        if self._get_value(S4APSettings.INDEX) is not None:
            logger.debug('Index found')
            if index == 0:
                logger.debug('Index is 0')
                return False
            elif self._get_value(S4APSettings.INDEX) + 1 == index:  # Index doesn't match
                logger.debug('Index matches')
                self.set_index_value(index)
                return False
            else:
                logger.debug('Index mismatched')
                print_json(True, 'sync.json')
                return True
        else:
            logger.debug("Storing initial index")
            self.set_index_value(index)
            return False

    def save_seed_values(self, host_name: str, port: str, seed_name: str, player: str):
        """ Overwrite Session specific values. """
        self._set_value(S4APSettings.SEED_NAME, seed_name)
        self._set_value(S4APSettings.HOST_NAME, host_name)
        self._set_value(S4APSettings.PORT_NUMBER, port)
        self._set_value(S4APSettings.PLAYER, player)
        S4APUtils.trigger_autosave()
        logger.debug("Session data saved successfully")

    def set_index_value(self, index: str):
        logger.debug(f'index: {index}')
        self._set_value(S4APSettings.INDEX, index)

    def save_item_info(self, items: str, item_ids: str, locations: str, senders: str):
        self._set_value(S4APSettings.ITEMS, items)
        self._set_value(S4APSettings.ITEM_IDS, item_ids)
        self._set_value(S4APSettings.LOCATIONS, locations)
        self._set_value(S4APSettings.SENDERS, senders)
        S4APUtils.trigger_autosave()

    def save_goal_and_career(self, goal: str, career: str):
        self._set_value(S4APSettings.GOAL, goal)
        self._set_value(S4APSettings.CAREER, career)
        S4APUtils.trigger_autosave()

    def get_items(self) -> str:
        return self._get_value(S4APSettings.ITEMS)

    def get_item_ids(self) -> str:
        return self._get_value(S4APSettings.ITEM_IDS)

    def get_locations(self) -> str:
        return self._get_value(S4APSettings.LOCATIONS)

    def get_senders(self) -> str:
        return self._get_value(S4APSettings.SENDERS)

    def get_seed_name(self) -> str:
        return self._get_value(S4APSettings.SEED_NAME)

    def get_goal(self) -> str:
        return self._get_value(S4APSettings.GOAL)

    def get_career(self) -> str:
        return self._get_value(S4APSettings.CAREER)

    def _get_value(self, key: str) -> Any:
        generic_settings_data_store: S4APGenericDataStore = self._data_manager.get_generic_settings_data()
        return generic_settings_data_store.get_value_by_key(key)

    def _set_value(self, key: str, value: Any):
        generic_settings_data_store: S4APGenericDataStore = self._data_manager.get_generic_settings_data()
        return generic_settings_data_store.set_value_by_key(key, value)
