from s4ap.events.Utils.send_location_event import SendLocationEvent
from s4ap.jsonio.s4ap_json import print_json, read_json
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.utils.s4ap_generic_utils import S4APUtils
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification

logger = S4APLogger.get_log()
logger.enable()


json_list = read_json('locations_cached')

victorylist = {'Bodybuilder (Bodybuilder 4)', 'Painter Extraordinaire (Painter Extraordinaire 4)',
               'Bestselling Author (Bestselling Author 4)', 'Musical Genius (Musical Genius 4)',
               'Public Enemy (Public Enemy 4)', 'Chief of Mischief (Chief of Mischief 4)',
               'Successful Lineage (Successful Lineage 4)', 'Big Happy Family (Big Happy Family 4)',
               'Master Mixologist (Master Mixologist 4)', 'Master Chef (Master Chef 4)',
               'Fabulously Wealthy (Fabulously Wealthy 4)', 'Mansion Baron (Mansion Baron 4)',
               'Renaissance Sim (Renaissance Sim 4)', 'Computer Whiz (Computer Whiz 4)', 'Nerd Brain (Nerd Brain 4)',
               'Soulmate (Soulmate 4)', 'Serial Romantic (Serial Romantic 4)',
               'Freelance Botanist (Freelance Botanist 4)', 'Angling Ace (Angling Ace 4)',
               'The Curator (The Curator 4)', 'Joke Star (Joke Star 4)', 'Friend of the World (Friend of the World 4)',
               'Party Animal (Party Animal 4)', 'Villainous Valentine (Villainous Valentine 1)',
               'Neighborly Advisor (Neighborhood Confidante 1)'}


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_send_check_event(event_data: SendLocationEvent):
    from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
    data_store = S4APSessionStoreUtils()
    global json_list
    if json_list is None and data_store.get_seed_name() is not None:
        json_list = {"Locations": [], "Seed": data_store.get_seed_name()}
    if event_data.location_name not in json_list["Locations"]:
        json_list["Locations"].append(event_data.location_name)
        print_json(json_list, 'locations_cached.json')
        notif = CommonBasicNotification(
            title_identifier='Saving on check',
            description_identifier=event_data.location_name
        )
        notif.show()
        S4APUtils.trigger_autosave()
