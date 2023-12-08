from typing import Any

from s4ap.enums.S4APLocalization import S4APIconId
from sims4communitylib.utils.common_icon_utils import CommonIconUtils


class S4APIconUtils(CommonIconUtils):
    @staticmethod
    def load_ap_logo_blue_icon() -> Any:
        """load_ap_logo_blue_icon()

        Get the Resource Key for the AP_LOGO_BLUE.

        :return: An identifier for the icon.
        :rtype: Any
        """
        return CommonIconUtils._load_icon(S4APIconId.AP_LOGO_BLUE)
