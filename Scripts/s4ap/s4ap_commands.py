from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from sims4communitylib.services.commands.common_console_command import CommonConsoleCommand
from sims4communitylib.services.commands.common_console_command_output import CommonConsoleCommandOutput

log = S4APLogger.get_log()
log.enable()


@CommonConsoleCommand(ModInfo.get_identity(), 's4ap.version', 'Prints the mod version to the console')
def _show_mod_version(output: CommonConsoleCommandOutput):
    output(f"The Sims 4 Archipelago, Current Mod Version: {ModInfo.get_identity().version}")
