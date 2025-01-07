import re

from s4ap.events.checks.send_check_event import SendLocationEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from sims.sim_info import SimInfo
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from statistics.skill import Skill

logger = S4APLogger.get_log()


class SimSkillLeveledUpEvent(CommonEvent):

    def __init__(self, sim_info: SimInfo, skill: Skill, new_skill_level: int):
        self._sim_info = sim_info
        self._skill = skill
        self._new_skill_level = new_skill_level

    @property
    def new_skill_level(self) -> int:
        """The level the Sim will be after leveling up."""
        return self._new_skill_level

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that leveled up in a Skill."""
        return self._sim_info

    @property
    def skill(self) -> Skill:
        """The Skill that was leveled up."""
        return self._skill

    @property
    def skill_id(self) -> int:
        """The decimal identifier of the Skill."""
        return CommonSkillUtils.get_skill_id(self.skill)


class HandleSkillLevelUp(CommonService):
    def _on_skill_updated(self, skill: Skill, new_skill_level: int) -> None:
        if skill.tracker is None or skill.tracker._owner is None:
            return
        if not skill.tracker._owner.is_npc:
            sim_info = CommonSimUtils.get_sim_info(skill.tracker._owner)
            CommonEventRegistry.get().dispatch(SimSkillLeveledUpEvent(sim_info, skill, new_skill_level))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Skill, Skill._handle_skill_up.__name__)
def _common_on_sim_skill_level_up(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    HandleSkillLevelUp.get()._on_skill_updated(self, *args, **kwargs)
    return result


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _on_skill_level_up(event_data: SimSkillLeveledUpEvent):
    if event_data.new_skill_level < 2:
        return None
    skill_id = event_data.skill.skill_type.__name__.replace("statistic_Skill_AdultMajor_", '')
    skill_id = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', skill_id).lower()
    if 'fitness' in skill_id:
        location_name = skill_id.replace('skill_', '')
    elif 'homestyle' in skill_id:
        location_name = skill_id.replace('homestyle ', '')
    elif 'gourmet' in skill_id:
        location_name = skill_id.replace("cooking ", "")
    elif 'bartending' in skill_id:
        location_name = skill_id.replace('bartending', 'mixology')
    else:
        location_name = skill_id
    logger.debug(f'Skill leveled up:{location_name}')
    location_name = f'{location_name.title()} Skill {event_data.new_skill_level}'
    CommonEventRegistry.get().dispatch(SendLocationEvent(location_name))
