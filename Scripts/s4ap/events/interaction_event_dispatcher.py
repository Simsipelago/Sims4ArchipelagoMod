import re

from protocolbuffers.Consts_pb2 import description
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from sims4communitylib.events.interaction.events.interaction_started import S4CLInteractionStartedEvent
from sims4communitylib.events.interaction.events.interaction_pre_run import S4CLInteractionPreRunEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.utils.resources.common_interaction_utils import CommonInteractionUtils
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.enums.icons_enum import CommonIconId
from ui.ui_dialog_notification import UiDialogNotification
from s4ap.enums.interactions import BLOCKED_INTERACTIONS

logger = S4APLogger.get_log()
logger.enable()

SKIP_LOGGING = ['sim-stand', 'mixer_AtWork_Default', 'sim-standExclusive', 'stand_Passive']

def show_blocked_interaction_notification(sim, interaction_name, description_identifier=None):
    """ Show a notification to the player when an interaction is blocked. """
    notification = CommonBasicNotification(
        title_identifier='Interaction Blocked!', # Title: "Alert!"
        description_identifier=f"{sim.first_name} {sim.last_name} was blocked from doing '{interaction_name}'",
        urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
    )
    notification.show()

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _on_interaction_started(event_data: S4CLInteractionStartedEvent):
    interaction = event_data.interaction
    interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction)
    interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
    sim = event_data.sim_info

    # Check if the Sim is part of the active household
    if not CommonHouseholdUtils.is_part_of_active_household(sim):
        return  # Ignore Sims outside the household

    if interaction_name in SKIP_LOGGING:
        return # avoid logging this interaction

    # Log interaction attempt
    logger.debug(f"Sim {sim} attempting interaction: {interaction_name} (ID: {interaction_id})")

    # Check if the interaction is blocked
    if interaction_id in BLOCKED_INTERACTIONS:
        logger.debug(f"Blocked interaction: {interaction_name} (ID: {interaction_id}) for Sim {sim}")
        show_blocked_interaction_notification(sim, interaction_name)

        # Cancel the interaction
        CommonSimInteractionUtils.cancel_interaction(interaction, "Blocked Interaction")

# @CommonEventRegistry.handle_events(ModInfo.get_identity())
# def _on_interaction_pre_run(event_data: S4CLInteractionPreRunEvent):
#     """ Cancel blocked interactions before they are fully executed. """
#     interaction = event_data.interaction
#     interaction_name = CommonInteractionUtils.get_interaction_short_name(interaction)
#     interaction_id = CommonInteractionUtils.get_interaction_id(interaction)
#     sim = event_data.interaction.sim.sim_info
#
#     # Check if the Sim is part of the active household
#     if not CommonHouseholdUtils.is_part_of_active_household(sim):
#         return  # Ignore Sims outside the household
#
#     if interaction_name in SKIP_LOGGING:
#         return # avoid logging this interaction
#
#     logger.debug(f"Sim {sim} attempting interaction: {interaction_name} (ID: {interaction_id})")
#
#     # Block interaction if it's in the blocked list
#     if interaction_id in BLOCKED_INTERACTIONS:
#         logger.debug(f"Blocking interaction: {interaction_name} (ID: {interaction_id}) for Sim {sim}")
#         show_blocked_interaction_notification(sim, interaction_name)
#
#         # **Cancel the interaction before it fully runs**
#         CommonSimInteractionUtils.cancel_interaction(interaction, "Blocked Interaction")