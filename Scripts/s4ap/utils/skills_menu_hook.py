import sims4.resources as resources
from s4ap.modinfo import ModInfo
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils
from ui.ui_dialog_picker import UiSkillsSimPicker
from s4ap.logging.s4ap_logger import S4APLogger
import services

# Initialize logger
logger = S4APLogger.get_log()
logger.enable()

# Check if the function exists before injecting
if hasattr(UiSkillsSimPicker, "_build_customize_picker"):
    logger.info("✅ _build_customize_picker exists and is being injected into!")
else:
    logger.error("❌ _build_customize_picker does NOT exist! Injection may fail!")

@CommonInjectionUtils.inject_safely_into(ModInfo.get_identity(), UiSkillsSimPicker, "_build_customize_picker")
def _show_all_skills(original, self, picker_data, *args, **kwargs):
    logger.info("✅ Successfully injected into _build_customize_picker!")

    original(self, picker_data, *args, **kwargs)  # Call the original function

    if not picker_data or not hasattr(picker_data, "sim_picker_data"):
        logger.error("❌ picker_data is invalid or missing sim_picker_data")
        return

    logger.debug(f"📌 picker_data.sim_picker_data.row_data count: {len(picker_data.sim_picker_data.row_data)}")

    for row in picker_data.sim_picker_data.row_data:
        sim_info = services.sim_info_manager().get(row.sim_id)
        if sim_info is None:
            logger.warning(f"⚠️ SimInfo not found for Sim ID {row.sim_id}")
            continue

        logger.debug(f"🔍 Processing Sim: {sim_info.full_name} (ID: {row.sim_id})")

        all_skills = services.get_instance_manager(resources.Types.STATISTIC).get_all()

        for skill in all_skills:
            if not getattr(skill, 'is_skill', False):  # Ensure it's a skill
                continue

            if not hasattr(row, "skills"):
                logger.error(f"🚨 Row has no 'skills' attribute for Sim {sim_info.full_name}")
                continue

            skill_data = row.skills.add()
            skill_data.skill_id = skill.guid64
            skill_data.current_points = int(sim_info.get_stat_value(skill)) if sim_info.has_statistic(skill) else 0
            skill_data.tooltip = skill.stat_name

            logger.debug(f"✅ Added skill: {skill.stat_name} (ID: {skill.guid64}) | Points: {skill_data.current_points}")

    logger.info("✅ Skill injection complete!")