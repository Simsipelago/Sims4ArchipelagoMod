from protocolbuffers.Localization_pb2 import LocalizedString

from lib.typing import Any
from sims4.localization import LocalizationHelperTuning, _create_localized_string, create_tokens

class S4APLocalizationUtils:

    @staticmethod
    def localize(string_object, tokens=()):
        tokens = S4APLocalizationUtils._localize_tokens(tokens)
        if isinstance(string_object, str):
            string_object = LocalizationHelperTuning.get_raw_text(string_object)
        else:
            if isinstance(string_object, int):
                return _create_localized_string(string_object, tokens)
            if hasattr(string_object, 'populate_localization_token'):
                return string_object
            if isinstance(string_object, LocalizedString):
                create_tokens(string_object.tokens, tokens)
                return string_object
            elif isinstance(string_object, LocalizedString):
                create_tokens(string_object.tokens, tokens)
                return string_object
        if isinstance(string_object, LocalizedString):
            create_tokens(string_object.tokens, tokens)
            return string_object

    @staticmethod
    def _localize_tokens(tokens_unlocalized):
        tokens = list()
        for token in tokens_unlocalized:
            tokens.append(S4APLocalizationUtils.localize(token))
        return tokens

    @staticmethod
    def create_from_string(string_text: str) -> LocalizedString:
        """create_from_string(string_text)

        Create a LocalizedString from a string.

        :param string_text: The string to localize. The resulting LocalizedString will be '{0.String}'
        :type string_text: str
        :return: A LocalizedString created from the specified string.
        :rtype: LocalizedString
        """
        return LocalizationHelperTuning.get_raw_text(string_text)

    @staticmethod
    def create_from_int(identifier: int, *tokens: Any) -> LocalizedString:
        """create_from_int(identifier, *tokens)

        Locate a LocalizedString by an identifier and format tokens into it.

        :param identifier: A decimal number that identifies an existing LocalizedString.
        :type identifier: int
        :param tokens: A collection of objects to format into the LocalizedString. (Example types: LocalizedString, str, int, etc.)
        :type tokens: Iterator[Any]
        :return: A LocalizedString with the specified tokens formatted into it.
        :rtype: LocalizedString
        """
        return _create_localized_string(identifier, *tokens)