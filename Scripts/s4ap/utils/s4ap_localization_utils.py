from protocolbuffers.Localization_pb2 import LocalizedString
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