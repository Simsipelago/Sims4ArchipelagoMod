import re

import services
from typing import Callable, Iterator, Union
from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.events.skill_events import SimSkillLeveledUpEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from s4ap.utils.s4ap_household_utils import S4APHouseholdUtils
from s4ap.utils.s4ap_sim_utils import S4APSimUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims4.resources import Types
from s4ap.utils.s4ap_skill_utils_class import S4APSkillUtils
from s4ap.sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from statistics.skill import Skill

logger = S4APLogger.get_log()
logger.enable()

def lock_skills(skillcap: int, skill_name, from_level_up: bool):
    try:
        logger.debug(f"Processing level up for {skill_name}")
        logger.debug(f"Skill cap is {skillcap}")
        data_store = S4APSessionStoreUtils()
        if skillcap < 2:
            skillcap = 2
        if not skill_name.startswith("statistic_Skill_AdultMajor_") and not 'fitness' in skill_name.lower():
            skill_name = f"statistic_Skill_AdultMajor_{skill_name}"
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
        if 'gourmet' in trait:
            trait = "lock_gourmet_cooking_skill"
        logger.debug(f"Skill Id: {skill_id}")
        logger.debug(f"Trait: {trait}")
        skill = TunableInstanceParam(Types.STATISTIC)(skill_name)
        for sim_info in S4APHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            current_level = S4APSkillUtils.get_current_skill_level(sim_info, skill)
            logger.debug(f"{S4APSimUtils.get_sim_first_name(sim_info)}'s Current {skill_id} level is {current_level}.")
            if skillcap > current_level:
                logger.debug(f"{skill_id} skill cap is greater than current level, unlocking skill.")
                remove_lock_trait(sim_info, trait)
            elif skillcap == current_level:
                logger.debug(f"{skill_id} skill cap is the same as the current level, locking skill.")
                add_lock_trait(sim_info, trait)
            elif skillcap < current_level:
                logger.debug(f"{skill_id} skill cap is less than current level, locking skill and setting skill level to {skillcap}")
                S4APSkillUtils.set_current_skill_level(sim_info, skill, skillcap)
                add_lock_trait(sim_info, trait)
    except Exception as ex:
        logger.debug(f"Exception occurred: {ex}")

def add_lock_trait(sim_info, trait):
    trait_upper = trait.upper()
    if hasattr(S4APTraitId, trait_upper):
        trait_id = getattr(S4APTraitId, trait_upper)
        trait_instance = TunableInstanceParam(Types.TRAIT)(trait_id)
        if not sim_info.has_trait(trait_instance):
            sim_info.add_trait(trait_instance)
        logger.debug(trait_id)
    logger.debug(trait_upper)


def remove_lock_trait(sim_info, trait):
    trait_upper = trait.upper()
    if hasattr(S4APTraitId, trait_upper):
        trait_id = getattr(S4APTraitId, trait_upper)
        trait_instance = TunableInstanceParam(Types.TRAIT)(trait_id)
        if sim_info.has_trait(trait_instance):
            sim_info.remove_trait(trait_instance)
        logger.debug(trait_id)
    logger.debug(trait_upper)


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _lock_on_level_up(event_data: SimSkillLeveledUpEvent):
    skill_name = event_data.skill.skill_type.__name__
    lock_skills(event_data.new_skill_level, skill_name, True)