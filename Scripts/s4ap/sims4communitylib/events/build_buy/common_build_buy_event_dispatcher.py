"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from typing import Any

from s4ap.sims4communitylib.events.build_buy.events.build_buy_enter import S4CLBuildBuyEnterEvent
from s4ap.sims4communitylib.events.build_buy.events.build_buy_exit import S4CLBuildBuyExitEvent
from s4ap.sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from s4ap.sims4communitylib.logging.has_class_log import HasClassLog
from s4ap.sims4communitylib.mod_support.mod_identity import CommonModIdentity
from s4ap.sims4communitylib.modinfo import ModInfo
from s4ap.sims4communitylib.services.common_service import CommonService
from s4ap.sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from zone import Zone


class CommonBuildBuyEventDispatcherService(CommonService, HasClassLog):
    """A service that dispatches Build/Buy events.

    .. warning:: Do not use this service directly to listen for events!\
        Use the :class:`.CommonEventRegistry` to listen for dispatched events.

    """

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_mod_identity(cls) -> CommonModIdentity:
        return ModInfo.get_identity()

    # noinspection PyMissingOrEmptyDocstring
    @classmethod
    def get_log_identifier(cls) -> str:
        return 's4cl_build_buy_event_dispatcher'

    def _on_build_buy_enter(self, zone: Zone, *_, **__):
        return CommonEventRegistry.get().dispatch(S4CLBuildBuyEnterEvent(zone))

    def _on_build_buy_exit(self, zone: Zone, *_, **__):
        return CommonEventRegistry.get().dispatch(S4CLBuildBuyExitEvent(zone))


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.on_build_buy_enter.__name__)
def _common_build_buy_enter(original, self, *args, **kwargs) -> Any:
    try:
        result = original(self, *args, **kwargs)
    except Exception as ex:
        CommonBuildBuyEventDispatcherService.get_log().format_error_with_message('An error occurred when performing Zone.on_build_buy_enter. (This exception is not caused by S4CL, but rather caught)', owner=self, argles=args, kwargles=kwargs, exception=ex)
        return
    CommonBuildBuyEventDispatcherService.get()._on_build_buy_enter(self, *args, **kwargs)
    return result


@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), Zone, Zone.on_build_buy_exit.__name__)
def _common_build_buy_exit(original, self, *args, **kwargs) -> Any:
    try:
        result = original(self, *args, **kwargs)
    except Exception as ex:
        CommonBuildBuyEventDispatcherService.get_log().format_error_with_message('An error occurred when performing Zone.on_build_buy_exit. (This exception is not caused by S4CL, but rather caught)', owner=self, argles=args, kwargles=kwargs, exception=ex)
        return
    CommonBuildBuyEventDispatcherService.get()._on_build_buy_exit(self, *args, **kwargs)
    return result
