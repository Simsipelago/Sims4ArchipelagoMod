import re

from protocolbuffers.Consts_pb2 import description
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from sims4communitylib.events.interaction.events.interaction_started import S4CLInteractionStartedEvent
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

BLOCKED_INTERACTIONS = {14241, 40413, 14426, 14427, 13443, 151354, 14428, 13439, 13950, 13952, 39965}

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