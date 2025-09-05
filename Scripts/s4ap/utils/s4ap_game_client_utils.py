import services
from server.clientmanager import ClientManager

class S4APGameClientUtils:

    @staticmethod
    def get_first_game_client() -> Union[Client, None]:
        """get_first_game_client()

        Retrieve an instance of the first available Game Client.

        :return: An instance of the first available Game Client or None if not found.
        :rtype: Union[Client, None]
        """
        client_manager = S4APGameClientUtils.get_game_client_manager()
        if client_manager is None:
            return None
        return client_manager.get_first_client()

    @staticmethod
    def get_game_client_manager() -> ClientManager:
        """get_game_client_manager()

        Retrieve the manager that manages the Game Clients for the game.

        :return: The manager that manages the Game Clients for the game.
        :rtype: ClientManager
        """
        return services.client_manager()