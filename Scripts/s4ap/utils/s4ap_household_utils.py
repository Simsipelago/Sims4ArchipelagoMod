import services
from services import active_household
from typing import Iterator, Union
from sims.household import Household
from sims.sim_info import SimInfo

class S4APHouseholdUtils:

    @classmethod
    def get_active_household(cls) -> Union[Household, None]:
        return services.active_household()

    @classmethod
    def get_sim_info_of_all_sims_in_active_household_generator(cls) -> Iterator[SimInfo]:
        household = active_household()
        if household is not None:
            for sim_info in household.sim_info_gen():
                if sim_info is not None:
                    yield sim_info