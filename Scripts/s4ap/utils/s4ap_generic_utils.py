import services
from typing import Union
from s4ap.modinfo import ModInfo
from services.persistence_service import SaveGameData
from sims4.resources import Types
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from s4ap.utils.s4ap_save_utils import S4APSaveUtils
from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog_notification import UiDialogNotification

class S4APUtils:

    @staticmethod
    def trigger_autosave(*_) -> bool:
        try:
            if CommonZoneSpinEventDispatcher().game_loading or not CommonZoneSpinEventDispatcher().game_loaded:
                return False
            import sims4.commands
            save_game_data = SaveGameData(S4APSaveUtils.get_save_slot_id(), 'S4APAutosave', True,
                                          5000002)
            persistence_service = services.get_persistence_service()
            persistence_service.save_using(persistence_service.save_game_gen, save_game_data, send_save_message=True,
                                           check_cooldown=False)
            return True
        except Exception as ex:
            S4APUtils.show_basic_notification(
                'A problem occured while saving S4AP Data',
                0
            )
            CommonExceptionHandler.log_exception(ModInfo.get_identity(), 'An exception occurred while autosaving.',
                                                 exception=ex)
            return False

    @staticmethod
    def load_instance(self, instance_type: Types, instance_id: int):
        """Load a resource instance (Trait, Buff, Mood, etc.) directly from the game."""
        instance_manager = services.get_instance_manager(instance_type)
        if instance_manager is None:
            return None
        return instance_manager.get(instance_id)

    @staticmethod
    def load_icon_by_id(icon_id: int):
        manager = services.get_instance_manager(Types.PNG)
        return manager.get(icon_id)  # Returns vanilla ResourceKey / instance

    @staticmethod
    def show_basic_notification(title_text: Union[int, str], description_text: Union[int, str]):
        """Show a simple vanilla notification to the player."""
        title = LocalizationHelperTuning.get_raw_text(title_text)
        description = LocalizationHelperTuning.get_raw_text(description_text)

        dialog = UiDialogNotification.TunableFactory().default(
            title=title,
            text=description
        )
        dialog.show_dialog()