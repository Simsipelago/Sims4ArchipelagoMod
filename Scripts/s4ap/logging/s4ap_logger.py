from s4ap.enums.S4APLocalization import S4APStringId
from s4ap.modinfo import ModInfo
from s4ap.utils.s4ap_generic_utils import S4APUtils
from s4ap.utils.s4ap_localization_utils import S4APLocalizationUtils
from s4ap.sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from s4ap.sims4communitylib.events.zone_spin.events.zone_late_load import S4CLZoneLateLoadEvent
from s4ap.sims4communitylib.logging.has_class_log import HasClassLog
from s4ap.sims4communitylib.mod_support.mod_identity import CommonModIdentity

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
        S4APUtils.show_basic_notification(
            S4APLocalizationUtils.localize(S4APStringId.S4AP_LOADED),
            'Loaded Sims 4 Archipelago Mod (' + ModInfo.get_identity().version + ')'
        )

    @staticmethod
    @CommonEventRegistry.handle_events('s4ap_loaded')
    def _show_loaded_notification_when_loaded(event_data: S4CLZoneLateLoadEvent):
        if event_data.game_loaded:
            # If the game has not loaded yet, we don't want to show our notification.
            return
        S4APLogger.show_loaded_notification()
