import re

from aspirations.aspiration_types import AspriationType
from s4ap.enums.S4APLocalization import S4APTraitId, HashLookup, S4APBaseGameSkills
from s4ap.jsonio.s4ap_json import print_json
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims4.resources import Types
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_trait_added import S4CLSimTraitAddedEvent
from sims4communitylib.notifications.common_basic_notification import CommonBasicNotification
from sims4communitylib.utils.common_icon_utils import CommonIconUtils
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from sims4communitylib.utils.sims.common_career_utils import CommonCareerUtils
from sims4communitylib.utils.sims.common_household_utils import CommonHouseholdUtils
from sims4communitylib.utils.sims.common_sim_career_utils import CommonSimCareerUtils
from sims4communitylib.utils.sims.common_sim_skill_utils import CommonSimSkillUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ui.ui_dialog_picker import ObjectPickerRow

logger = S4APLogger.get_log()
logger.enable()


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_show_max_skills_phone(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.SHOW_RECEIVED_SKILLS:
        CommonTraitUtils.remove_trait(event_data.sim_info, S4APTraitId.SHOW_RECEIVED_SKILLS)
        data_store = S4APSessionStoreUtils()
        options = []
        skills_and_levels = {}
        if data_store.get_items() is not None:
            for item in data_store.get_items():
                if 'skill' not in item.lower() and not 'multiplier' in item.lower():
                    continue
                else:
                    item_count = data_store.get_items().count(item)
                    max_skill = item_count + 2
                    skills_and_levels[item] = max_skill
        option = 1
        skills = {}
        for skill in S4APBaseGameSkills.BASE_GAME_ADULT_SKILLS:
            if skill == "Fitness":
                skill_id = f'skill_Fitness'
            elif skill == "Homestyle Cooking":
                skill = skill.replace("Homestyle ", "")
                skill_id = f'statistic_Skill_AdultMajor_{skill}'
            elif skill == "Mixology":
                skill_id = f'statistic_Skill_AdultMajor_Bartending'
            elif skill == "Gourmet Cooking":
                str1 = skill[0:6]
                str2 = skill[8:14]
                skill = str1 + str2
                skill_id = f'statistic_skill_AdultMajor_{skill}'
            else:
                skill_id = f'statistic_Skill_AdultMajor_{skill}'
            skill_id = skill_id.replace(" ", "")
            skill_icon = TunableInstanceParam(Types.STATISTIC)(skill_id).icon
            max_skill = skills_and_levels.get(f"{skill} Skill")
            if max_skill is not None:
                if max_skill > 10:
                    max_skill = 10
            skills[skill] = [max_skill, skill_icon]
        for item, item_info in sorted(skills.items()):
            options.append(ObjectPickerRow(
                option_id=option,
                name=CommonLocalizationUtils.create_localized_string(
                    f'{item} Max is {item_info[0] or 2}'),
                icon=item_info[1]
            ))
            option += 1

        def _on_chosen(_, outcome: CommonChoiceOutcome):
            if outcome == CommonChoiceOutcome.CHOICE_MADE:
                dialog.show(on_chosen=_on_chosen)

        dialog = CommonChooseObjectDialog(
            'Max Possible Skills',
            'The highest you can level your skills to.',
            choices=options
        )
        dialog.show(on_chosen=_on_chosen)

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _resync_locations(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.RESYNC_LOCATIONS:
        CommonTraitUtils.remove_trait(event_data.sim_info, S4APTraitId.RESYNC_LOCATIONS)
        lookup = HashLookup()
        locations = []
        skill_dict = {}
        careers_dict = {}
        for sim_info in CommonHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            for skill in CommonSkillUtils.get_all_skills_gen():
                skill_level = CommonSimSkillUtils.get_current_skill_level(sim_info, skill, False)
                skill_name = skill.skill_type.__name__
                if skill_name.startswith("statistic_Skill_AdultMajor_") or 'fitness' in skill_name.lower():
                    skill_name = skill_name.replace("statistic_Skill_AdultMajor_", "")
                else:
                    continue
                if 'flower' in skill_name.lower() or 'knitting' in skill_name.lower():
                    continue
                elif skill_dict.get(skill_name) is not None:
                    if skill_level > skill_dict.get(skill_name):
                        skill_dict[skill_name] = skill_level
                else:
                    skill_dict[skill_name] = skill_level
            for skill_old_name, skill_level in skill_dict.items():
                skill_id = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', skill_old_name).lower()
                if 'fitness' in skill_id:
                    skill_new_name = skill_id.replace('skill_', '')
                elif 'homestyle' in skill_id:
                    skill_new_name = skill_id.replace('homestyle ', '')
                elif 'gourmet' in skill_id:
                    skill_new_name = skill_id.replace(" cooking", "")
                elif 'bartending' in skill_id:
                    skill_new_name = skill_id.replace('bartending', 'mixology')
                else:
                    skill_new_name = skill_id
                for level in range(2, int(skill_level) + 1):
                    location_name = f'{skill_new_name.title()} Skill {level}'
                    locations.append(location_name)
            for career in CommonSimCareerUtils.get_all_careers_for_sim_gen(sim_info):
                career_id = CommonCareerUtils.get_career_guid(career)
                career_level = career.user_level
                if careers_dict.get(career_id) is not None:
                    if career_level > careers_dict.get(career_id):
                        careers_dict[career_id] = career_level
                else:
                    careers_dict[career_id] = career_level
            for career_guid, level in careers_dict.items():
                career = CommonCareerUtils.load_career_by_guid(career_guid)
                for i in range(1, level + 1):
                    (_, _, career_track) = CommonCareerUtils.determine_entry_level_into_career_from_user_level(career, i)
                    career_hash =  career_track.get_career_name(sim_info).hash
                    career_name = lookup.get_career_name(career_hash, i)
                    if career_name is not None:
                        locations.append(career_name)
            milestones = sim_info.aspiration_tracker._completed_milestones
            for milestone in milestones:
                if milestone.aspiration_type != AspriationType.FULL_ASPIRATION:
                    continue
                elif milestone.is_valid_for_sim(sim_info) and milestone.display_name is not None:
                    milestone_display_name = lookup.get_display_name(milestone.display_name)
                    if milestone_display_name is not None:
                        locations.append(milestone_display_name)
        print_json(locations, 'locations_cached.json')
        print_json(True, 'sync.json')
        notif = CommonBasicNotification(
            'Locations Resynced',
            ''
        )
        notif.show()

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _show_aspiration_and_career(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.SHOW_YAML_OPTIONS:
        CommonTraitUtils.remove_trait(event_data.sim_info, S4APTraitId.SHOW_YAML_OPTIONS)
        data_store = S4APSessionStoreUtils()
        if data_store.get_goal() is not None:
            goal = data_store.get_goal()
        else:
            goal = 'Cant find the aspiration'
        if data_store.get_career() is not None:
            career = data_store.get_career()
        else:
            career = 'Cant find the career'
        if data_store.get_items() is not None:
            item = 'Skill Gain Multiplier'
            if data_store.get_items().count(item) is not None:
                item_count = data_store.get_items().count(item)
                if item_count == 1:
                    display = '2.5 Skill Multiplier'
                elif item_count == 2:
                    display = '3 Skill Multiplier'
                elif item_count == 3:
                    display = '3.5 Skill Multiplier'
                elif item_count >= 4:
                    display = '4 Skill Multiplier'
                else:
                    display = 'No Skill Multiplier'
            else:
                display = 'No Skill Multiplier'
        else:
            display = 'No Skill Multiplier'
        def _on_chosen(_, outcome: CommonChoiceOutcome):
            if outcome == CommonChoiceOutcome.CHOICE_MADE:
                dialog.show(on_chosen=_on_chosen)
        options = [
            ObjectPickerRow(
                option_id=1,
                name= CommonLocalizationUtils.create_localized_string(goal.replace("_", " ").title()),
                icon= CommonIconUtils.load_icon_by_id(1903793975082081275)
            ),
            ObjectPickerRow(
                option_id=2,
                name= CommonLocalizationUtils.create_localized_string(career.replace("_", " ").title()),
                icon= CommonIconUtils.load_icon_by_id(12028399282094277793)
            ),
            ObjectPickerRow(
                option_id=3,
                name= CommonLocalizationUtils.create_localized_string(display),
                icon= CommonIconUtils.load_icon_by_id(5906963266871873908)
            )
        ]

        dialog = CommonChooseObjectDialog(
            'Your Yaml Options Plus Skill Multiplier',
            'Options + Skill Multiplier',
            choices=options
        )
        dialog.show(on_chosen=_on_chosen)
