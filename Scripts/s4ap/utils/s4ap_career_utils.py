import services
from s4ap.utils.s4ap_localization_utils import localize
from server_commands.argument_helpers import TunableInstanceParam
from s4ap.enums.s4ap_enums import Icon, Option
from sims4.resources import Types, get_resource_key
from ui.ui_dialog_picker import ObjectPickerRow

def change_career_branches(career_type:TunableInstanceParam(Types.CAREER), _connection=None):

    def _picker_row_callback(result_tag=None):
        if result_tag is Option.CHANGE_CAREER_BRANCH:
            career.career_stop()
            career._current_track = career.start_track
            career._level = len(career.start_track.career_levels) - 1
            career._user_level = len(career.start_track.career_levels)
            career._overmax_level = 0
            career._reset_career_objectives(career.start_track, career._level)
            career._sim_info.career_tracker.update_history(career)
            career.career_start()
            career.resend_career_data()
            career.resend_at_work_info()
            career.promote()

    client = services.client_manager().get(_connection)
    sim_info = client.active_sim_info
    if career_type is None or sim_info is None:
        return
    career = sim_info.career_tracker.get_career_by_uid(career_type.guid64)
    picker_rows = []
    if career._current_track != career.start_track:
        picker_rows.append(
            ObjectPickerRow(
                option_id=Option.CHANGE_CAREER_BRANCH,
                name=localize('Change Career Branch'),
                icon_id=get_resource_key(Icon.JOB, Types.PNG),
            ))