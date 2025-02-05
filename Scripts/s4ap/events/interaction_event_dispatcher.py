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

TOILET_INTERACTIONS = {151354, 13443, 14427, 40413, 14426, 213986, 212233, 14428, 14431, 226929, 309868, 14433, 14434, 155887, 14432, 99479}

SHOWER_INTERACTIONS = {13439, 13950, 13952, 110817, 154397, 39965, 110818, 24332, 110819, 23839, 110820, 141926, 39860, 110821, 39845, 110822, 185951, 35123, 227358, 13949, 96785, 212246, 227343, 227344}

SINK_INTERACTIONS = {14241, 14238, 14240, 133052, 74885, 132167, 222271, 14239, 220557, 29854, 220559, 132168, 100109, 100104, 14242, 212217, 36844, 212219, 212088, 212221}

BATH_INTERACTIONS = {13427, 35352, 120467, 13085, 120473, 120474, 120475, 121800, 121804, 121802, 213938, 215915, 215876, 215764}

BATHROOM_INTERACTIONS = {*TOILET_INTERACTIONS, *SHOWER_INTERACTIONS, *SINK_INTERACTIONS, *BATH_INTERACTIONS}

WORK_INTERACTIONS = {23936, 23930, 97665}

FRIDGE_INTERACTIONS = {13397, 100327, 13388, 13395, 31030, 13387, 152488, 13389, 13390, 152489, 26331, 26361, 152490, 37405, 37404, 75761, 159769, 159768, 76891, 76893, 76895, 76897, 76899, 76901, 76903, 76905, 26319, 164448, 270682, 111967, 217063, 77672, 164355, 156400, 156402, 156404, 156403, 37208}

COUNTER_INTERACTIONS = {13276, 13277, 13269, 13263, 13268, 269311, 37780, 29829}

STOVE_INTERACTIONS = {14337, 32043, 14343, 14331, 10163, 76907, 76909, 76911, 76913, 76915, 76917, 76919, 76921, 75766, 37343, 14338, 212642, 37788, 37789, 14344, 212301, }

OVEN_INTERACTIONS = {13770, 270725, 37782}

COOKING_INTERACTIONS = {13434, 13263, 13257}

KITCHEN_INTERACTIONS = {*FRIDGE_INTERACTIONS, *COUNTER_INTERACTIONS, *STOVE_INTERACTIONS, *OVEN_INTERACTIONS}

EATING_INTERACTIONS = {13433, 13377, 13378}

IDLE_INTERACTIONS = {13481}

NEED_INTERACTIONS = {13994, 77557, 13993, 14029}

BED_INTERACTIONS = {100082, 13094, 151428, 13091}

SLEEP_INTERACTIONS = {9230, 96864, 100071, 28880}

BLOCKED_INTERACTIONS = {*BATHROOM_INTERACTIONS, *KITCHEN_INTERACTIONS, *WORK_INTERACTIONS, *NEED_INTERACTIONS, *SLEEP_INTERACTIONS, *IDLE_INTERACTIONS, *COOKING_INTERACTIONS}

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