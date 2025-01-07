import services
from s4ap.modinfo import ModInfo
from services.persistence_service import SaveGameData
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.save_load.common_save_utils import CommonSaveUtils


class S4APUtils:

    @staticmethod
    def trigger_autosave(*_) -> bool:
        try:
            if CommonZoneSpinEventDispatcher().game_loading or not CommonZoneSpinEventDispatcher().game_loaded:
                return False
            import sims4.commands
            save_game_data = SaveGameData(CommonSaveUtils.get_save_slot_id(), 'S4APAutosave', True,
                                          5000002)
            persistence_service = services.get_persistence_service()
            persistence_service.save_using(persistence_service.save_game_gen, save_game_data, send_save_message=True,
                                           check_cooldown=False)
            return True
        except Exception as ex:
            CommonBasicNotification(
                'A problem occured while saving S4AP Data',
                0
            ).show()
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An exception occurred while autosaving.',
                                                 exception=ex)
            return False
