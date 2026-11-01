from dataclasses import dataclass
from statistics.skill import Skill
from typing import Optional

from sims.sim_info import SimInfo


@dataclass
class SimSkillLeveledUpEvent:
    _sim_info: SimInfo
    _skill: Skill
    _new_skill_level: int

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
    def skill_id(self) -> Optional[int]:
        """The decimal identifier of the Skill, or None if the Skill has no guid64 attribute."""
        from s4ap.utils.s4ap_skill_utils_class import S4APSkillUtils
        return S4APSkillUtils.get_skill_id(self.skill)
