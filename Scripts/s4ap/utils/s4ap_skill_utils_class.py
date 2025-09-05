import services
from typing import Callable, Iterator, Union
from s4ap.utils.s4ap_sim_utils import S4APSimUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims.sim_info import SimInfo
from sims4.resources import Types
from statistics.skill import Skill

class S4APSkillUtils:

    @staticmethod
    def get_current_skill_level(sim_info: SimInfo, skill: TunableInstanceParam(Types.STATISTIC)) -> float:
        skill_stat = sim_info.get_statistic(skill, add=False)
        if skill_stat is None:
            return 0.0
        skill_level: float = skill_stat.get_user_value()
        return skill_level

    @staticmethod
    def set_current_skill_level(sim_info: SimInfo, skill: TunableInstanceParam(Types.STATISTIC), level: float) -> bool:
        skill_stat = sim_info.get_statistic(skill, add=False)
        if skill_stat is None:
            return False
        exp = skill_stat.convert_from_user_value(level)
        skill_stat.set_value(exp)
        return True

    @staticmethod
    def get_all_skills_available_for_sim_gen(sim_info: SimInfo) -> Iterator[Skill]:
        sim = S4APSimUtils.get_sim_instance(sim_info)
        if sim is None:
            return tuple()

        def _is_skill_available_for_sim(skill: Skill) -> bool:
            return skill.can_add(sim)

        yield from S4APSkillUtils.get_all_skills_gen(include_skill_callback=_is_skill_available_for_sim)

    @staticmethod
    def get_all_skills_gen(include_skill_callback: Callable[[Skill], bool] = None) -> Iterator[Skill]:
        statistic_manager = services.get_instance_manager(Types.STATISTIC)
        for skill in statistic_manager.get_ordered_types(only_subclasses_of=Skill):
            skill: Skill = skill
            skill_id = S4APSkillUtils.get_skill_id(skill)
            if skill_id is None:
                continue
            if include_skill_callback is not None and not include_skill_callback(skill):
                continue
            yield skill

    @staticmethod
    def get_skill_id(skill_identifier: Union[int, Skill]) -> Union[int, None]:
        """get_skill_id(skill_identifier)

        Retrieve the decimal identifier of a Skill.

        :param skill_identifier: The identifier or instance of a Skill.
        :type skill_identifier: Union[int, Skill]
        :return: The decimal identifier of the Skill or None if the Skill does not have an id.
        :rtype: Union[int, None]
        """
        if isinstance(skill_identifier, int):
            return skill_identifier
        return getattr(skill_identifier, 'guid64', None)