from typing import Any

import services

class S4APSaveUtils:

    @staticmethod
    def get_save_slot() -> Any:
        """get_save_slot()

        Retrieve the current save slot.

        :return: The current save slot.
        :return: Any
        """
        return services.get_persistence_service().get_save_slot_proto_buff()

    @staticmethod
    def get_save_slot_id() -> int:
        """get_save_slot_id()

        Retrieve the identifier for the current save slot.

        :return: The identifier for the current save slot.
        :return: int
        """
        return S4APSaveUtils.get_save_slot().slot_id