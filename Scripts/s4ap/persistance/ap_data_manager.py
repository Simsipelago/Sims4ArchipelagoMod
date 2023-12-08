from typing import Tuple

from s4ap.modinfo import ModInfo
from sims4communitylib.mod_support.mod_identity import CommonModIdentity
from sims4communitylib.persistence.data_management.common_data_manager import CommonDataManager
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.persistence_services.common_persistence_service import CommonPersistenceService


@CommonDataManagerRegistry.common_data_manager()
class S4APDataManager(CommonDataManager):
    """ Manage checks sent, items received and points spent
    Also has to store Seed, hostname and Port to enable the game to send a warning if any of those change
     """

    @property
    def mod_identity(self) -> CommonModIdentity:
        # This Mod identity is what distinguishes your data manager from other mods. Use the ModInfo from your own project!
        return ModInfo.get_identity()

    @property
    def log_identifier(self) -> str:
        return 's4ap_data_manager'

    @property
    def persistence_services(self) -> Tuple[CommonPersistenceService]:
        from sims4communitylib.persistence.persistence_services.common_file_persistence_service import \
            CommonFilePersistenceService
        result: Tuple[CommonPersistenceService] = (
            CommonFilePersistenceService(per_save=True, per_save_slot=False),
        )
        return result
