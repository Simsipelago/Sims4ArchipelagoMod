from typing import Any, Union

import services

class S4APSaveUtils:

    @staticmethod
    def get_save_slot() -> Any:
        """get_save_slot()

        Retrieve the current save slot.

        :return: The current save slot.
        :return: Union[int, None]
        """
        persistence_service = services.get_persistence_service()
        if persistence_service is None:
            return None
        return persistence_service.get_save_slot_proto_buff()

    @staticmethod
    def get_save_slot_id() -> Union[int, None]:
        """get_save_slot_id()

        Retrieve the identifier for the current save slot.

        :return: The identifier for the current save slot.
        :return: int
        """
        save_slot = S4APSaveUtils.get_save_slot()
        if save_slot is None:
            return None
        return save_slot.slot_id