from sims.sim_info import SimInfo

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