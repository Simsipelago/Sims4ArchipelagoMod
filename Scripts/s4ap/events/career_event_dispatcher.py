from careers.career_base import CareerBase
from s4ap.enums.S4APLocalization import HashLookup
from s4ap.events.checks.send_check_event import SendLocationEvent
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.utils.s4ap_sim_utils import S4APSimUtils
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.services.common_service import CommonService
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils

log = S4APLogger.get_log()
log.enable()


class CareerPromotionEvent(CommonEvent):
    def __init__(self, career, current_level):
        self._career = career
        self._current_level = current_level

    @property
    def career(self):
        return self._career

    @property
    def current_level(self):
        return self._current_level


class OnCareerPromotionEvent(CommonService):

    def _on_promotion(self, career, user_level: int, name: str, *_, **__):
        career_name = HashLookup().get_career_name(career, user_level)
        log.debug(f'here is the career: {career} {user_level} ({career_name})')
        log.debug(f'{name} was promoted to {career_name}')
        CommonEventRegistry.get().dispatch(CareerPromotionEvent(career, user_level))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), CareerBase,
                                         CareerBase._handle_promotion.__name__, handle_exceptions=True)
def _on_milestone_complete(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)
    career = self._current_track.get_career_name(self._sim_info).hash
    level = self._user_level
    sim_info = self._sim_info
    if sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
        sim_name = S4APSimUtils.get_sim_first_name(sim_info)
        OnCareerPromotionEvent.get()._on_promotion(career, level, sim_name)
    return result


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _send_notif_on_event_handle(event_data: CareerPromotionEvent):
    lookup = HashLookup()
    CommonEventRegistry.get().dispatch(
        SendLocationEvent(f'{lookup.get_career_name(event_data.career, event_data.current_level)}'))
