from sims4communitylib.events.event_handling.common_event import CommonEvent


class SendCheckEvent(CommonEvent):

    def __init__(self, location_id: int):
        self._location_id = location_id

    @property
    def location_id(self):
        return self._location_id
