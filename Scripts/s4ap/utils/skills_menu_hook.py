from sims4.resources import Types
import services
import sims4
from ui.ui_dialog_picker import UiSkillsSimPicker

# Store the original function so we can call it later
_original_build_customize_picker = UiSkillsSimPicker._build_customize_picker

def _patched_build_customize_picker(self, picker_data):
    # Call the original method first to retain existing functionality
    _original_build_customize_picker(self, picker_data)

    # Add all skills, even if the Sim hasn't gained experience in them
    for row in picker_data.sim_picker_data.row_data:
        sim_info = services.sim_info_manager().get(row.sim_id)
        all_skills = services.get_instance_manager(Types.STATISTIC).get_ordered_types(class_restrictions=('Skill',))

        for skill in all_skills:
            skill_data = row.skills.add()
            skill_data.skill_id = skill.guid64
            skill_data.current_points = int(
                sim_info.get_stat_value(skill.skill_type) or 0)  # Default to 0 if uninitialized
            skill_data.tooltip = skill.stat_name

# Override the method in the class
UiSkillsSimPicker._build_customize_picker = _patched_build_customize_picker