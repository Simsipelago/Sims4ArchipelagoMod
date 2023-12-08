from typing import Type, Union, Dict, Any

from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_data_manager import S4APDataManager
from s4ap.persistance.ap_data_store import S4APGenericDataStore
from sims4communitylib.persistence.data_management.common_data_manager_registry import CommonDataManagerRegistry
from sims4communitylib.persistence.data_stores.common_data_store import CommonDataStore
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput
from sims4communitylib.services.common_service import CommonService


class S4APDataManagerUtils(CommonService):
    """ Utilities for accessing data stores """

    def __init__(self) -> None:
        self._data_manager: S4APDataManager = None

    @property
    def data_manager(self) -> S4APDataManager:
        """ The data manager containing data. """
        if self._data_manager is None:
            self._data_manager: S4APDataManager = CommonDataManagerRegistry().locate_data_manager(
                ModInfo.get_identity())
        return self._data_manager

    # We will discuss this function a bit later in the tutorial!
    def _get_data_store(self, data_store_type: Type[CommonDataStore]) -> Union[CommonDataStore, None]:
        return self.data_manager.get_data_store_by_type(data_store_type)

    def get_all_data(self) -> Dict[str, Dict[str, Any]]:
        """ Get all data. """
        return self.data_manager._data_store_data

    def get_generic_settings_data(self) -> S4APGenericDataStore:
        """ Retrieve the Generic Settings Data Store. """
        data_store: S4APGenericDataStore = self._get_data_store(S4APGenericDataStore)
        return data_store

    def save(self) -> bool:
        """ Save data. """
        return self.data_manager.save()

    def reset(self, prevent_save: bool = False) -> bool:
        """ Reset data. """
        return self.data_manager.remove_all_data(prevent_save=prevent_save)


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap_test.data_store_test', 'Test Dialog')
def _test_data_store(output: CommonConsoleCommandOutput):
    pass
