from sims.sim_info import SimInfo

class S4APSimCurrencyUtils:

    @classmethod
    def add_simoleons_to_household(cls, sim_info: SimInfo, amount: int, reason: int, **kwargs) -> bool:
        """
        Add an amount of simoleons to the Household of a Sim.

        :param sim_info: The Sim whose household to modify.
        :param amount: The number of simoleons to add (negative values will subtract).
        :param reason: A string reason for the funds change (from Consts_pb2).
        :return: True if successful, False otherwise.
        """
        if sim_info is None or sim_info.household is None:
            return False

        funds = sim_info.household.funds
        if funds is None:
            return False

        funds.add(amount, reason, **kwargs)
        return True
