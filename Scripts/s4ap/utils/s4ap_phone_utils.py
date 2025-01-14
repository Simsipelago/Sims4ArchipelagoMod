import re

from s4ap.enums.S4APLocalization import S4APTraitId
from s4ap.logging.s4ap_logger import S4APLogger
from s4ap.modinfo import ModInfo
from s4ap.persistance.ap_session_data_store import S4APSessionStoreUtils
from sims4communitylib.dialogs.choose_object_dialog import CommonChooseObjectDialog
from sims4communitylib.dialogs.common_choice_outcome import CommonChoiceOutcome
from sims4communitylib.events.event_handling.common_event_registry import CommonEventRegistry
from sims4communitylib.events.sim.events.sim_trait_added import S4CLSimTraitAddedEvent
from sims4communitylib.utils.localization.common_localization_utils import CommonLocalizationUtils
from sims4communitylib.utils.resources.common_skill_utils import CommonSkillUtils
from sims4communitylib.utils.sims.common_trait_utils import CommonTraitUtils
from ui.ui_dialog_picker import ObjectPickerRow

logger = S4APLogger.get_log()
logger.enable()


@CommonEventRegistry.handle_events(ModInfo.get_identity())
def _handle_show_max_skills_phone(event_data: S4CLSimTraitAddedEvent):
    if event_data.trait_id == S4APTraitId.SHOW_RECEIVED_SKILLS:
        CommonTraitUtils.remove_trait(event_data.sim_info, S4APTraitId.SHOW_RECEIVED_SKILLS)
        data_store = S4APSessionStoreUtils()
        options = set()
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
        for skill in CommonSkillUtils.get_all_skills_gen():
            skill_id = skill.skill_type.__name__
            if 'fitness' in skill_id.lower() or skill_id.startswith(
                    "statistic_Skill_AdultMajor_") and not 'knitting' in skill_id.lower() and not 'flower' in skill_id.lower():
                skill_name = skill_id.replace("statistic_Skill_AdultMajor_", '')
                skill_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', skill_name).lower()
                if 'fitness' in skill_name:
                    skill_name = skill_name.replace('skill_', '')
                elif 'homestyle' in skill_name:
                    skill_name = skill_name.replace('homestyle ', '')
                elif 'gourmet' in skill_name:
                    skill_name = skill_name.replace("cooking ", "")
                elif 'bartending' in skill_name:
                    skill_name = skill_name.replace('bartending', 'mixology')
                skill_name = skill_name.title()
                max_skill = skills_and_levels.get(f"{skill_name} Skill")
                if max_skill is not None:
                    if max_skill > 10:
                        max_skill = 10
                options.add(ObjectPickerRow(
                    option_id=option,
                    name=CommonLocalizationUtils.create_localized_string(
                        f'{skill_name} Max is {max_skill or 2}'),
                    icon=skill.icon
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
