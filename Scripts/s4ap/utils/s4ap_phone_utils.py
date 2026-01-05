import re

from aspirations.aspiration_types import AspriationType
from lot51_core.utils.dialog import DialogHelper
from s4ap.enums.S4APLocalization import S4APTraitId, HashLookup, S4APBaseGameSkills
from s4ap.jsonio.s4ap_json import print_json
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from s4ap.utils.s4ap_career_utils import S4APCareerUtils
from s4ap.utils.s4ap_dialog_utils import S4APDialog
from s4ap.utils.s4ap_generic_utils import S4APUtils
from s4ap.utils.s4ap_household_utils import S4APHouseholdUtils
from s4ap.utils.s4ap_skill_utils_class import S4APSkillUtils
from server_commands.argument_helpers import TunableInstanceParam
from sims4.localization import LocalizationHelperTuning
from sims4.resources import Types
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_trait_added import S4CLSimTraitAddedEvent
from ui.ui_dialog_picker import ObjectPickerRow

logger = S4APLogger.get_log()
logger.enable()


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_show_max_skills_phone(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.SHOW_RECEIVED_SKILLS:
        received_skills_trait_instance = TunableInstanceParam(Types.TRAIT)(S4APTraitId.SHOW_RECEIVED_SKILLS)
        if event_data.sim_info.has_trait(received_skills_trait_instance):
            event_data.sim_info.remove_trait(received_skills_trait_instance)
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
                skill_id = f'statistic_Skill_AdultMajor_{skill}'
                skill = skill.replace("Homestyle ", "")
            elif skill == "Mixology":
                skill_id = f'statistic_Skill_AdultMajor_Bartending'
            elif skill == "Gourmet Cooking":
                skill_id = f'statistic_skill_AdultMajor_Gourmetcooking'
                skill = "Gourmet"
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
                name = LocalizationHelperTuning.get_raw_text(f'{item} Max is {item_info[0] or 2}'),
                icon=item_info[1]
            ))
            option += 1

        sim = event_data.sim_info.get_sim_instance()

        picker = S4APDialog.ObjectPickerDialog(
            sim=sim,
            title='Max Possible Skills',
            text='The highest you can level your skills to.',
            picker_rows=options
        )

        picker.show_dialog()

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _resync_locations(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.RESYNC_LOCATIONS:
        resync_trait_instance = TunableInstanceParam(Types.TRAIT)(S4APTraitId.RESYNC_LOCATIONS)
        if event_data.sim_info.has_trait(resync_trait_instance):
            event_data.sim_info.remove_trait(resync_trait_instance)
        lookup = HashLookup()
        locations = []
        skill_dict = {}
        careers_dict = {}
        for sim_info in S4APHouseholdUtils.get_sim_info_of_all_sims_in_active_household_generator():
            for skill in S4APSkillUtils.get_all_skills_gen():
                skill_level = S4APSkillUtils.get_current_skill_level(sim_info, skill)
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
            for career in S4APCareerUtils.get_all_careers_for_sim_gen(sim_info):
                career_id = S4APCareerUtils.get_career_guid(career)
                career_level = career.user_level
                if careers_dict.get(career_id) is not None:
                    if career_level > careers_dict.get(career_id):
                        careers_dict[career_id] = career_level
                else:
                    careers_dict[career_id] = career_level
            for career_guid, level in careers_dict.items():
                career = S4APCareerUtils.load_career_by_guid(career_guid)
                for i in range(1, level + 1):
                    (_, _, career_track) = S4APCareerUtils.determine_entry_level_into_career_from_user_level(career, i)
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
        DialogHelper.create_notification(
            'Locations Resynced',
            ''
        ).show_dialog()

@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _show_aspiration_and_career(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.SHOW_YAML_OPTIONS:
        yaml_options_trait_instance = TunableInstanceParam(Types.TRAIT)(S4APTraitId.SHOW_YAML_OPTIONS)
        if event_data.sim_info.has_trait(yaml_options_trait_instance):
            event_data.sim_info.remove_trait(yaml_options_trait_instance)
        data_store = S4APSessionStoreUtils()
        if data_store.get_goal() is not None:
            goal = data_store.get_goal()
        else:
            goal = "Can't find the aspiration"

        options = [
            (1, LocalizationHelperTuning.get_raw_text(goal.replace("_", " ").title()), 1903793975082081275),
        ]

        row_id = 2

        # ---------- Careers Header ----------
        options.append((
            row_id,
            LocalizationHelperTuning.get_raw_text("──────── Careers ────────"),
            0
        ))
        row_id += 1

        # ---------- Careers ----------
        career_data = data_store.get_career()

        if career_data:
            if isinstance(career_data, list):
                for career in career_data: # list with items in it
                    options.append(
                        (row_id,
                         LocalizationHelperTuning.get_raw_text(career.replace("_", " ").title()),
                         12028399282094277793)
                    )
                    row_id += 1
        else: # none or empty list
            options.append(
                (row_id,
                 LocalizationHelperTuning.get_raw_text("Can't find the career"),
                 12028399282094277793)
            )
            row_id += 1

        # ---------- Skill Multiplier ----------
        options.append((
            row_id,
            LocalizationHelperTuning.get_raw_text("──────── Skill Bonus ────────"),
            0
        ))
        row_id += 1

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

        options.append(
            (row_id, LocalizationHelperTuning.get_raw_text(display), 5906963266871873908)
        )

        # ---------- Show Picker ----------

        sim = event_data.sim_info.get_sim_instance()

        picker = S4APDialog.ObjectPickerDialog(
            sim=sim,
            title='Your Yaml Options Plus Skill Multiplier',
            text='Options + Skill Multiplier',
            picker_rows=options
        )

        picker.show_dialog()
