import services
from s4ap.utils.s4ap_localization_utils import S4APLocalizationUtils
from sims4.resources import Types, get_resource_key
from ui.ui_dialog_picker import ObjectPickerRow, ObjectPickerType, UiObjectPicker

class S4APDialog:

    class ObjectPickerDialog:

        def __init__(self, sim=None, title=str(), text=str(), picker_rows=None, min_selectable=1, max_selectable=1,
                     is_sortable=False, picker_type=ObjectPickerType.OBJECT, callback=None):
            self.sim = sim
            self.title = S4APLocalizationUtils.localize(title)
            self.text = S4APLocalizationUtils.localize(text)
            self.picker_rows = picker_rows if picker_rows else []
            self.min_selectable = min_selectable
            self.max_selectable = max_selectable
            self.is_sortable = is_sortable
            self.picker_type = picker_type
            self.callback = callback

        def show_dialog(self):
            object_picker = UiObjectPicker.TunableFactory().default(self.sim, text=lambda *args, **kwargs: self.text,
                                                                    title=lambda *args, **kwargs: self.title,
                                                                    min_selectable=self.min_selectable,
                                                                    max_selectable=self.max_selectable,
                                                                    is_sortable=self.is_sortable,
                                                                    picker_type=self.picker_type)
            for picker_row in self.picker_rows:
                if picker_row is not None:
                    if isinstance(picker_row, ObjectPickerRow):
                        object_picker.add_row(picker_row)
                    else:
                        object_picker.add_row(picker_row.get_object_picker_row())
            if self.callback:
                object_picker.add_listener(self._internal_callback)
            object_picker.show_dialog()

        def _internal_callback(self, dialog):
            result_tags = dialog.get_result_tags()
            for tag in result_tags:
                self.callback(result_tag=tag)

        @staticmethod
        def create_picker_row(option_id, title=str(), text=str(), rarity_text=str(), object_id=None, def_id=None,
                              icon_id=None, tag=None, is_enable=True):
            name = S4APLocalizationUtils.localize(title)
            row_description = S4APLocalizationUtils.localize(text)
            rarity_text = S4APLocalizationUtils.localize(rarity_text)
            if icon_id is not None:
                icon = get_resource_key(icon_id, Types.PNG)
            else:
                icon = None
            if tag is None:
                tag = option_id
            return ObjectPickerRow(option_id=option_id, name=name, row_description=row_description,
                                   rarity_text=rarity_text, object_id=object_id, def_id=def_id, icon=icon, tag=tag,
                                   count=0, is_enable=is_enable)