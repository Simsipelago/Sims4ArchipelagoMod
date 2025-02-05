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

logger = S4APLogger.get_log()
logger.enable()

TOILET_INTERACTIONS = {151354, 13443, 14427, 40413, 14426, 213986}

SHOWER_INTERACTIONS = {13439, 13950, 13952, 110817, 154397, 39965, 110818, 24332, 110819, 23839, 110820, 141926, 39860, 110821, 39845, 110822, 185951}

SINK_INTERACTIONS = {14241, 14238, 14240, 133052, 74885, 132167}

BATH_INTERACTIONS = {13427, 35352, 120467, 13085, 120473, 120474, 120475, 121800, 121804, 121802, 213938, 215915, 215876, 215764}

BATHROOM_INTERACTIONS = {*TOILET_INTERACTIONS, *SHOWER_INTERACTIONS, *SINK_INTERACTIONS, *BATH_INTERACTIONS}

WORK_INTERACTIONS = {23936, 23930, 97665}

FRIDGE_INTERACTIONS = {13397, 100327}

EATING_INTERACTIONS = {13433, 13377, 13378}

IDLE_INTERACTIONS = {13481, }

NEED_INTERACTIONS = {13994, 77557}

BLOCKED_INTERACTIONS = {14428, *BATHROOM_INTERACTIONS, *WORK_INTERACTIONS, *FRIDGE_INTERACTIONS, *NEED_INTERACTIONS}

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

    SKIP_LOGGING = ['sim-stand', 'mixer_AtWork_Default', 'sim-standExclusive']


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
#     logger.debug(f"Sim {sim} attempting interaction: {interaction_name} (ID: {interaction_id})")
#
#     # Block interaction if it's in the blocked list
#     if interaction_id in BLOCKED_INTERACTIONS:
#         logger.debug(f"Blocking interaction: {interaction_name} (ID: {interaction_id}) for Sim {sim}")
#         show_blocked_interaction_notification(sim, interaction_name)
#
#         # **Cancel the interaction before it fully runs**
#         CommonSimInteractionUtils.cancel_interaction(interaction, "Blocked Interaction")