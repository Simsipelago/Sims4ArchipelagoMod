from sims4communitylib.events.event_handling.common_event import CommonEvent


class AllowReceiveItems(CommonEvent):

    def __init__(self, is_allowed: bool):
        self._is_allowed = is_allowed

    @property
    def is_allowed(self):
        return self._is_allowed
