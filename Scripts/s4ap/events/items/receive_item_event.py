from sims4communitylib.events.event_handling.common_event import CommonEvent


class ReceiveItemEvent(CommonEvent):
    # [{"cmd":"ReceivedItems","index":0,"items":[{"item":80000,"location":-1,"player":0,"flags":0,"class":"NetworkItem"}]}]
    def __init__(self, item_id: int):
        self._item_id = item_id

    @property
    def item_id(self):
        return self._item_id
