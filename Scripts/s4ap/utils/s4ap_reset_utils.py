from lot51_core.utils.dialog import DialogHelper
from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.utils.s4ap_generic_utils import S4APUtils
from s4ap.utils.s4ap_household_utils import S4APHouseholdUtils
from s4ap.utils.s4ap_skill_utils_class import S4APSkillUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4communitylib.enums.traits_enum import CommonTraitId
from ui.ui_dialog_notification import UiDialogNotification

logger = S4APLogger.get_log()
logger.enable()

class ResetSimData:
    def reset_all_skills(self):
        for sim_info in S4APHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            for skill in S4APSkillUtils.get_all_skills_available_for_sim_gen(sim_info):
                sim_info.remove_statistic(skill)

    def show_reset_notif(self):
        DialogHelper.create_notification(
            'Progress Reset Completed',
            "Your Sim's skills have been successfully reset. Please switch to a different sim or leave the lot and revisit to ensure the changes are visible in the UI."
        ).show_dialog()

    def remove_all_s4ap_traits(self):
        # Get all traits from the base class CommonTraitId
        common_trait_ids = set(vars(CommonTraitId).keys())
        for trait, trait_value in vars(S4APTraitId).items():
            # Check if the trait is not a built-in attribute and is unique to S4APTraitId
            if not trait.startswith("_") and trait not in common_trait_ids:
                logger.debug(f"Removing trait {trait}: {trait_value}")
                trait_instance = TunableInstanceParam(Types.TRAIT)(trait_value)
                for sim_info in S4APHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
                    if sim_info.has_trait(trait_instance):
                        sim_info.remove_trait(trait_instance)
