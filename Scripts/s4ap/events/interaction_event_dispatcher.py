import re

from protocolbuffers.Consts_pb2 import description
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from sims4communitylib.events.interaction.events.interaction_started import S4CLInteractionStartedEvent
from sims4communitylib.events.interaction.events.interaction_pre_run import S4CLInteractionPreRunEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_interaction_utils import CommonSimInteractionUtils
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.enums.strings_enum import CommonStringId
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.enums.icons_enum import CommonIconId
from ui.ui_dialog_notification import UiDialogNotification

logger = S4APLogger.get_log()
logger.enable()

BLOCKED_INTERACTIONS = {14428}

TOILET_INTERACTIONS = {151354, 13443, 14427, 40413, 14426, 213986}

SHOWER_INTERACTIONS = {13439, 13950, 13952, 110817, 154397, 39965, 110818, 24332, 110819, 23839, 110820, 141926, 39860, 110821, 39845, 110822, 104658, 104659, 185951, 141216, 141928}

SINK_INTERACTIONS = {14241}

BATH_INTERACTIONS = {13427, 35352, 120467, 13085, 120473, 120474, 120475, 121800, 121804, 121802, 213938, 215915, 215876, 215764}

BATHROOM_INTERACTIONS = {*TOILET_INTERACTIONS, *SHOWER_INTERACTIONS, *SINK_INTERACTIONS}

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
    interaction_name = getattr(event_data.interaction.affordance, 'instance_name', str(event_data.interaction.affordance))
    sim = event_data.sim_info
    interaction_id = getattr(event_data.interaction, "guid64", None)  # Use None if not available
    if interaction_id is None:
        interaction_id = getattr(event_data.interaction, "id", None)  # Try "id" as a fallback

    # Check if the Sim is part of the active household
    if not CommonHouseholdUtils.is_part_of_active_household(sim):
        return  # Ignore Sims outside the household

    # Log interaction attempt
    logger.debug(f"Sim {sim} attempting interaction: {interaction_name} (ID: {interaction_id})")

    # Check if the interaction is blocked
    if interaction_id in BLOCKED_INTERACTIONS:
        logger.debug(f"Blocked interaction: {interaction_name} (ID: {interaction_id}) for Sim {sim}")

        # Cancel the interaction
        CommonSimInteractionUtils.cancel_interaction(interaction, "Blocked Interaction")

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _on_interaction_pre_run(event_data: S4CLInteractionPreRunEvent):
    """ Cancel blocked interactions before they are fully executed. """
    interaction = event_data.interaction
    interaction_name = getattr(interaction.affordance, 'instance_name', str(interaction.affordance))
    sim = event_data.interaction.sim.sim_info
    interaction_id = getattr(interaction, "guid64", None) or getattr(interaction, "id", None)  # Fallback

    # Check if the Sim is part of the active household
    if not CommonHouseholdUtils.is_part_of_active_household(sim):
        return  # Ignore Sims outside the household

    logger.debug(f"Sim {sim} attempting interaction: {interaction_name} (ID: {interaction_id})")

    # Block interaction if it's in the blocked list
    if interaction_id in BLOCKED_INTERACTIONS:
        logger.debug(f"Blocking interaction: {interaction_name} (ID: {interaction_id}) for Sim {sim}")
        show_blocked_interaction_notification(sim, interaction_name)

        # **Cancel the interaction before it fully runs**
        CommonSimInteractionUtils.cancel_interaction(interaction, "Blocked Interaction")