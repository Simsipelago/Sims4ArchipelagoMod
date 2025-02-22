import re

from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.events.skill_event_dispatcher import SimSkillLeveledUpEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims4.resources import Types
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_name_utils import CommonSimNameUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils

logger = S4APLogger.get_log()
logger.enable()


def lock_skills(skillcap: int, skill_name, from_level_up: bool):
    try:
        logger.debug(f"Skill cap is {skillcap}")
        data_store = S4APSessionStoreUtils()
        if skillcap < 2:
            skillcap = 2
        if not skill_name.startswith("statistic_Skill_AdultMajor_") and not 'fitness' in skill_name.lower():
            skill_name = f"statistic_Skill_AdultMajor_{skill_name}"
        logger.debug(f'{skill_name}')
        skill_id = skill_name.replace("statistic_Skill_AdultMajor_", '')
        skill_id = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', skill_id)
        if 'bartending' in skill_id.lower():
            skill_id = skill_id.lower().replace('bartending', 'mixology')
        if from_level_up is True and data_store.get_items() is not None:
            skill_id_lower = skill_id.replace("_", " ").strip().lower()
            item_name = skill_id_lower
            if 'fitness' in skill_id_lower:
                item_name = skill_id_lower.replace('skill', '').strip()
            elif 'homestyle' in skill_id_lower:
                item_name = skill_id_lower.replace('homestyle', '').strip()
            elif 'gourmet' in skill_id_lower:
                item_name = skill_id_lower.replace("cooking", "").strip()
            elif 'bartending' in skill_id_lower:
                item_name = skill_id_lower.replace('bartending', 'mixology').strip()
            logger.debug(f"item_name: {item_name}")
            for item in data_store.get_items():
                if item_name in item.lower():
                    skillcap = data_store.get_items().count(item) + 2
                    logger.debug(f"new skillcap: {skillcap}")
                    break
                else:
                    continue
        trait = f"lock_{skill_id.lower().replace('skill_', '')}_skill"
        logger.debug(f"Skill Id: {skill_id}")
        logger.debug(f"Trait: {trait}")
        skill = TunableInstanceParam(Types.STATISTIC)(skill_name)
        for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            current_level = CommonSimSkillUtils.get_current_skill_level(sim_info, skill, False)
            logger.debug(f"{CommonSimNameUtils.get_first_name(sim_info)}'s Current level is {current_level}.")
            if skillcap > current_level:
                logger.debug('Skill cap is > than current level')
                remove_lock_trait(sim_info, trait, skill_id)
            elif skillcap == current_level:
                logger.debug('Skill cap is == as current level')
                add_lock_trait(sim_info, trait)
            elif skillcap < current_level:
                logger.debug('Skill cap is < than current level')
                CommonSimSkillUtils.set_current_skill_level(sim_info, skill, skillcap)
                add_lock_trait(sim_info, trait)
    except Exception as ex:
        logger.debug(f"Exception occurred: {ex}")

def add_lock_trait(sim_info, trait):
    trait_upper = trait.upper()
    if hasattr(S4APTraitId, trait_upper):
        trait_id = getattr(S4APTraitId, trait_upper)
        CommonTraitUtils.add_trait(sim_info, trait_id)
        logger.debug(trait_id)
    logger.debug(trait_upper)


def remove_lock_trait(sim_info, trait, skill_id):
    trait_upper = trait.upper()
    if hasattr(S4APTraitId, trait_upper):
        trait_id = getattr(S4APTraitId, trait_upper)
        CommonTraitUtils.remove_trait(sim_info, trait_id)
        logger.debug(trait_id)
    logger.debug(f"Unlocking skill and removing trait {trait_upper} locking {skill_id} for Sim {CommonSimNameUtils.get_first_name(sim_info)}.")


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _lock_on_level_up(event_data: SimSkillLeveledUpEvent):
    skill_name = event_data.skill.skill_type.__name__
    lock_skills(event_data.new_skill_level, skill_name, True)
