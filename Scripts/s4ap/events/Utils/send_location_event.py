from sims4communitylib.events.event_handling.common_event import CommonEvent


class SendLocationEvent(CommonEvent):
    def __init__(self, location_name):
        self._location_name = location_name

    @property
    def location_name(self) -> str:
        return self._location_name