from sims4communitylib.mod_support.common_mod_info import CommonModInfo


class ModInfo(CommonModInfo):
    """ Mod info for randomizer Mod"""
    _FILE_PATH: str = str(__file__)

    @property
    def _name(self) -> str:
        # This is the name that'll be used whenever a Messages.txt or Exceptions.txt file is created
        # <_name>_Messages.txt and <_name>_Exceptions.txt.
        return 's4ap'

    @property
    def _version(self) -> str:
        # Mod version
        return '0.1.12'

    @property
    def _author(self) -> str:
        # This is your name.
        return 'Cactus'

    @property
    def _base_namespace(self) -> str:
        # This is the name of the root package
        return 's4ap'

    @property
    def _file_path(self) -> str:
        # This is simply a file path that you do not need to change.
        return ModInfo._FILE_PATH
