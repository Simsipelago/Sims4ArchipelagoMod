from aspirations.aspiration_types import AspriationType
from aspirations.aspirations import AspirationTracker
from s4ap.enums.S4APLocalization import HashLookup
from s4ap.events.checks.send_check_event import SendLocationEvent
from s4ap.modinfo import ModInfo
from s4ap.utils.s4ap_sim_utils import S4APSimUtils
from s4ap.sims4communitylib.events.event_handling.common_event import CommonEvent
from s4ap.sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from s4ap.sims4communitylib.services.common_service import CommonService
from lot51_core.utils.injection import inject_to


class MilestoneCompletion(CommonEvent):

    def __init__(self, aspiration_display_name, milestone_display_name, milestone_count):
        self._aspiration_display_name = aspiration_display_name
        self._milestone_display_name = milestone_display_name
        self._milestone_count = milestone_count

    @property
    def aspiration_display_name(self):
        return self._aspiration_display_name

    @property
    def milestone_display_name(self):
        return self._milestone_display_name

    @property
    def milestone_count(self):
        return self._milestone_count

@inject_to(AspirationTracker, AspirationTracker.complete_milestone.__name__)
def _on_milestone_complete(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    OnMilestoneCompletionEvent.get()._on_milestone_completion(*args, **kwargs)
    return result


class OnMilestoneCompletionEvent(CommonService):

    def _on_milestone_completion(self, aspiration, *_, **__):
        if aspiration.aspiration_type == AspriationType.FULL_ASPIRATION:
            if aspiration.is_valid_for_sim(S4APSimUtils.get_active_sim_info()):
                aspiration_display_name = aspiration.display_name
                track = S4APSimUtils.get_active_sim_info().primary_aspiration
                track_display_text = track.display_text  # this takes the primary aspiration name as a LocalizedString object
                return CommonEventRegistry.get().dispatch(
                    MilestoneCompletion(track_display_text, aspiration_display_name, aspiration))


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _send_notif_on_event_handle(event_data: MilestoneCompletion):
    lookup = HashLookup()
    CommonEventRegistry.get().dispatch(SendLocationEvent(lookup.get_display_name(event_data.milestone_display_name)))
