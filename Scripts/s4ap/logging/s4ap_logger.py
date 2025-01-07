from s4ap.enums.S4APLocalization import S4APStringId
from s4ap.modinfo import ModInfo
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from sims4communitylib.logging.has_class_log import HasClassLog
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils


class S4APLogger(HasClassLog):
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4ap_logger'

    @staticmethod
    def show_loaded_notification() -> None:
        """ Show that the mod has loaded. """
        notification = CommonBasicNotification(
            CommonLocalizationUtils.create_localized_string(S4APStringId.S4AP_LOADED),
            'Loaded Sims 4 Archipelago Mod (' + ModInfo.get_identity().version + ')'
        )
        notification.show()

    @staticmethod
    @CommonEventRegistry.handle_events('s4ap_loaded')
    def _show_loaded_notification_when_loaded(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            # If the game has not loaded yet, we don't want to show our notification.
            return
        S4APLogger.show_loaded_notification()
