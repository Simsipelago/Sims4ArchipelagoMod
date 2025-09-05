from lib.typing import Iterator, Optional, Union
from s4ap.utils.s4ap_generic_utils import S4APUtils
from sims.sim_info import SimInfo
from sims4.resources import Types
from traits.traits import Trait

class S4APTraitUtils:

    @classmethod
    def remove_traits(cls, sim_info: SimInfo, traits: Iterator[Union[int, Trait]]) -> bool:
        """Remove traits from a Sim using only vanilla TS4 API.

        :param sim_info: The Sim to remove the traits from.
        :param traits: An iterator of Trait instances or trait IDs.
        :return: True if all traits were successfully removed, False otherwise.
        """
        all_removed = True

        for trait_item in traits:
            trait = cls.load_trait_by_id(trait_item)
            if trait is None:
                all_removed = False
                continue

            if sim_info.has_trait(trait):
                if not sim_info.remove_trait(trait):
                    all_removed = False

        return all_removed

    @classmethod
    def load_trait_by_id(cls, trait) -> Optional['Trait']:
        if isinstance(trait, Trait):
            return trait

        try:
            trait_id = int(trait)
        except Exception:
            return None

        return S4APUtils.load_instance(Types.TRAIT, trait_id)