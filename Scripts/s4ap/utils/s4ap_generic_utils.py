import services
from typing import Any, Callable, Optional, Union

from lot51_core.utils.dialog import DialogHelper
from s4ap.modinfo import ModInfo
from s4ap.utils.s4ap_sim_utils import S4APSimUtils
from services.persistence_service import SaveGameData
from sims.sim_info import SimInfo
from sims4.resources import Types
from sims4communitylib.events.zone_spin.common_zone_spin_event_dispatcher import CommonZoneSpinEventDispatcher
from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from s4ap.utils.s4ap_save_utils import S4APSaveUtils
from sims4.localization import LocalizationHelperTuning
from ui.ui_dialog import UiDialogOkCancel
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
            owner=None,
            title=title,
            text=description
        )
        dialog.show_dialog()

    @classmethod
    def show_ok_cancel_dialog(
            cls,
            title,
            text,
            ok_text,
            cancel_text,
            on_ok: Optional[Callable[[UiDialogOkCancel], Any]] = None,
            on_cancel: Optional[Callable[[UiDialogOkCancel], Any]] = None,
            owner: Optional[SimInfo] = None
    ):
        """Show an Ok/Cancel dialog with optional handlers for each response.

        :param title: LocalizedString for the title.
        :param text: LocalizedString for the body text.
        :param ok_text: LocalizedString for the OK button.
        :param cancel_text: LocalizedString for the Cancel button.
        :param on_ok: Callback if the user presses OK.
        :param on_cancel: Callback if the user presses Cancel.
        :param owner: SimInfo or None (defaults to None).
        """

        active_sim = S4APSimUtils.get_active_sim_info()
        if active_sim is None:
            # Skip showing the dialog if no active sim yet
            return

        def _on_response(dialog_instance: UiDialogOkCancel):
            if dialog_instance.accepted:
                if on_ok is not None:
                    on_ok(dialog_instance)
            else:
                if on_cancel is not None:
                    on_cancel(dialog_instance)

        dialog = DialogHelper.create_dialog(
            title,
            text,
            ok_text,
            callback=_on_response
        )
        # dialog = UiDialogOkCancel.TunableFactory().default(
        #     active_sim,
        #     title=title,
        #     text=text,
        #     ok_text=ok_text,
        #     cancel_text=cancel_text
        # )



        # dialog.add_listener(_on_response)
        # dialog.show_dialog()
        return dialog