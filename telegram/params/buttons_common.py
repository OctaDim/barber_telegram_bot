from dataclasses import dataclass


@dataclass
class COMMON_BUTTONS_PARAMS:
    START = "🚀 Старт"
    MAIN_MENU = "📂 Главное Меню"
    SAY_BYE = "🚪 Say 'Bye-Bye'"
    RETURN = "↩️ Вернуться"


@dataclass
class CONFIRM_DIALOG_BUTTONS:
    YES = "ДА"
    NO = "НЕТ"


@dataclass
class SPECIAL_CHARACTERS:
    NO_ACTION_EMPTY_u200B = "\u200B"  # DO NOT CHANGE!!! ZERO-WIDTH EMPTY SYMBOL
    UNBROKEN_NON_ZERO_SPACE_u00A0 = "\u00A0"  # DO NOT CHANGE!!! UNBROKEN LEN SPACE SYMBOL
    MULTI_3_DOTS_u2026 = "\u2026"  # DO NOT CHANGE!!! MULTI DOTS SYMBOL
    NO_ACTION_SYMBOL_REPLY = "—"  # DO NOT DELETE, SPACE OR EMPY NOT ALLOWED IN REPLY!!!

    # Fot the future
    # FILL_IN_BLANK_SYMBOL = "\u0020"  # USING TO FILL IN BLANK SPACE WITH SPACES
