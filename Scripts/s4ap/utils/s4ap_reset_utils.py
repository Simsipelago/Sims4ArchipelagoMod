from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.logging.s4ap_logger import S4APLogger
from sims4communitylib.enums.traits_enum import CommonTraitId
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

logger = S4APLogger.get_log()
logger.enable()

class ResetSimData:
    def reset_all_skills(self):
        for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            for skill in CommonSimSkillUtils.get_all_skills_available_for_sim_gen(sim_info):
                CommonSimSkillUtils.remove_skill(sim_info, skill)

    def show_reset_notif(self):
        notif = CommonBasicNotification(
            'Progress Reset Completed',
            "Your Sim's skills have been successfully reset. Please switch to a different sim or leave the lot and revisit to ensure the changes are visible in the UI."
        )
        notif.show()

    def remove_all_s4ap_traits(self):
        # Get all traits from the base class CommonTraitId
        common_trait_ids = set(vars(CommonTraitId).keys())
        for trait, trait_value in vars(S4APTraitId).items():
            # Check if the trait is not a built-in attribute and is unique to S4APTraitId
            if not trait.startswith("_") and trait not in common_trait_ids:
                logger.debug(f"Removing trait {trait}: {trait_value}")
                for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
                    CommonTraitUtils.remove_trait(sim_info, trait_value)
