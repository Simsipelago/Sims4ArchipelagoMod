import time

from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from s4ap.utils.s4ap_skill_utils import lock_skills
from sims4communitylib.enums.common_currency_modify_reasons import CommonCurrencyModifyReason
from sims4communitylib.events.event_handling.common_event import CommonEvent
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.sims.common_career_utils import CommonCareerUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_career_utils import CommonSimCareerUtils
from sims4communitylib.utils.sims.common_sim_currency_utils import CommonSimCurrencyUtils
from sims4communitylib.utils.sims.common_sim_utils import CommonSimUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from collections import Counter
log = S4APLogger.get_log()
log.enable()


class ReceiveItemEvent(CommonEvent):
    def __init__(self, index: str, items: str, item_ids: str, locations: str, players: str):
        self._index = index
        self._items = items
        self._item_ids = item_ids
        self._locations = locations
        self._players = players

    @property
    def index(self) -> str:
        return self._index

    @property
    def items(self) -> str:
        return self._items

    @property
    def item_ids(self) -> str:
        return self._item_ids

    @property
    def locations(self) -> str:
        return self._locations

    @property
    def players(self) -> str:
        return self._players


class HandleReceiveItemEvent:

    @staticmethod
    @CommonEventRegistry.handle_events(ModInfo.get_identity())
    def _handle_receive_item_event(event_data: ReceiveItemEvent):
        data_store = S4APSessionStoreUtils()
        handle_item = HandleReceiveItemEvent()
        if data_store.check_index_value(event_data.index):  # If index matches, pass
            pass
        elif int(event_data.index) == 0:
            if (data_store.get_item_ids() and data_store.get_items() and data_store.get_senders() and data_store.get_locations()) is not None:
                if data_store.get_item_ids() != event_data.item_ids:
                    stored_items = list(zip(
                        data_store.get_items() or [],
                        data_store.get_item_ids() or [],
                        data_store.get_senders() or [],
                        data_store.get_locations() or []
                    ))

                    incoming_items = list(
                        zip(event_data.items, event_data.item_ids, event_data.players, event_data.locations))

                    # Use Counter to count occurrences in each list
                    stored_counter = Counter(stored_items)
                    incoming_counter = Counter(incoming_items)

                    # Subtract stored items from incoming items
                    filtered_counter = incoming_counter - stored_counter

                    # Convert back to a flat list of tuples
                    filtered_items = list(filtered_counter.elements())
                    item_info = list(zip(*filtered_items))

                    if item_info:
                        log.debug('item_info filtered')
                        log.debug(f"item_info items: {item_info[0]}")
                        data_store.save_item_info(event_data.items, event_data.item_ids, event_data.locations,
                                                  event_data.players)
                        handle_item.handle_items(item_info[0])
                        handle_item.show_received_notification(item_info[0], item_info[2], item_info[3])
                    else:
                        log.debug('No new items to handle')
                    log.debug('items handled')
            else:
                filtered_zipped = zip(  # filters out old items from the new ReceivedItems using item ids
                    *[(item, item_id, player, location) for item, item_id, player, location in
                      zip(event_data.items, event_data.item_ids, event_data.players, event_data.locations)
                      ]
                )
                item_info = list(filtered_zipped)
                data_store.save_item_info(event_data.items, event_data.item_ids, event_data.locations,
                                          event_data.players)
                if item_info:
                    handle_item.handle_items(item_info[0])
                    handle_item.show_received_notification(item_info[0], item_info[2], item_info[3])
                else:
                    log.debug('No new items to handle')
                log.debug('items handled')

        else:
            log.debug('Index is > than previous index')
            if data_store.get_items() is not None:
                updated_items = data_store.get_items() + event_data.items
                if data_store.get_item_ids() is not None:
                    updated_item_ids = data_store.get_item_ids() + event_data.item_ids
                    updated_locations = data_store.get_locations() + event_data.locations
                    updated_players = data_store.get_senders() + event_data.players
                    data_store.save_item_info(updated_items, updated_item_ids, updated_locations, updated_players)
                    handle_item.handle_items(event_data.items)
                    handle_item.show_received_notification(event_data.items, event_data.players, event_data.locations)
                # Combines both of the old and new items & item_ids and saves them

    def handle_items(self, items):
        data_store = S4APSessionStoreUtils()
        for item in items:  # For each item checked it either processes them as simoleons or as a different item
            log.debug(f'Processing {item}')
            if 'Simoleons' in item:  # Simoleon items are either '5000 Simoleons' or '2000 Simoleons'
                number = item.split()[0]
                CommonSimCurrencyUtils.add_simoleons_to_household(CommonSimUtils.get_active_sim_info(), int(number),
                                                                  CommonCurrencyModifyReason.CHEAT)
                time.sleep(0.2)
            elif 'boost' in item.lower():
                if 'career' in item.lower():
                    for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
                        for career in CommonSimCareerUtils.get_all_careers_for_sim_gen(sim_info):
                            if career is None:
                                break
                            old_work_performance = CommonCareerUtils.get_work_performance(career)
                            work_performance_left_to_add = 100 - old_work_performance
                            career.add_work_performance(work_performance_left_to_add)
                            career.resend_career_data()
            if 'multiplier' in item.lower():
                boost_count = data_store.get_items().count(item)
                if boost_count == 1:
                    add_trait = S4APTraitId.SKILL_GAIN_BOOST_2_5X
                    rem_traits = None
                elif boost_count == 2:
                    rem_traits = (S4APTraitId.SKILL_GAIN_BOOST_2_5X,)
                    add_trait = S4APTraitId.SKILL_GAIN_BOOST_3X
                elif boost_count == 3:
                    rem_traits = (S4APTraitId.SKILL_GAIN_BOOST_2_5X, S4APTraitId.SKILL_GAIN_BOOST_3X)
                    add_trait = S4APTraitId.SKILL_GAIN_BOOST_3_5X
                elif boost_count == 4:
                    rem_traits = (S4APTraitId.SKILL_GAIN_BOOST_2_5X, S4APTraitId.SKILL_GAIN_BOOST_3X,
                                  S4APTraitId.SKILL_GAIN_BOOST_3_5X)
                    add_trait = S4APTraitId.SKILL_GAIN_BOOST_4X
                for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
                    if rem_traits is not None:
                        CommonTraitUtils.remove_traits(sim_info, rem_traits)
                    CommonTraitUtils.add_trait(sim_info, add_trait)
            elif 'skill' in item.lower():
                count = data_store.get_items().count(item)
                count += 2
                skill = item.replace(" Skill", '').replace(" ", "")
                if 'fitness' in skill.lower():
                    skill = f"skill_{skill}"
                elif 'cooking' in skill.lower():
                    skill = f"homestyle{skill}"
                elif 'mixology' in skill.lower():
                    skill = skill.lower().replace('mixology', 'bartending')
                lock_skills(count, skill, False)

    def show_received_notification(self, items, players, locations):
        notif = CommonBasicNotification(
            title_identifier='Received Items',
            description_identifier='\n'.join(
                [f'{item} from {player} ({location})' for item, player, location in zip(items, players, locations)]))
        notif.show()
