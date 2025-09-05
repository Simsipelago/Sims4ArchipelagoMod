import services
from lib.typing import Union
from sims.sim import Sim
from sims.sim_info import SimInfo
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from sims.sim_info_manager import SimInfoManager

class S4APSimUtils:

    @staticmethod
    def get_sim_first_name(sim_info: SimInfo):
        if sim_info is None or not hasattr('first_name'):
            return ''
        return getattr(sim_info, 'first_name')

    @classmethod
    def get_sim_instance(cls, sim_identifier: SimInfo):
        if isinstance(sim_identifier, SimInfo):
            return sim_identifier.get_sim_instance()

    @classmethod
    def get_sim_info(
            cls,
            sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
    ) -> Union[SimInfo, SimInfoBaseWrapper, None]:
        """get_sim_info(sim_identifier)

        Retrieve a SimInfo instance from a Sim identifier.

        :param sim_identifier: The identifier or instance of a Sim to use.
        :type sim_identifier: Union[int, Sim, SimInfo, SimInfoBaseWrapper]
        :return: The SimInfo of the specified Sim instance or None if SimInfo is not found.
        :rtype: Union[SimInfo, SimInfoBaseWrapper, None]
        """
        if sim_identifier is None or isinstance(sim_identifier, SimInfo):
            return sim_identifier
        if isinstance(sim_identifier, SimInfoBaseWrapper):
            return sim_identifier.get_sim_info()
        if isinstance(sim_identifier, Sim):
            return sim_identifier.sim_info
        if isinstance(sim_identifier, int):
            return cls.get_sim_info_manager().get(sim_identifier)
        return sim_identifier

    @classmethod
    def get_sim_info_manager(cls) -> SimInfoManager:
        """get_sim_info_manager()

        Retrieve the manager that manages the Sim Info of all Sims in a game world.

        :return: The manager that manages the Sim Info of all Sims in a game world.
        :rtype: SimInfoManager
        """
        return services.sim_info_manager()