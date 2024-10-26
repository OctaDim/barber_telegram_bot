from dataclasses import dataclass


@dataclass
class COMMON_BUTTONS_PARAMS:
    START = "🚀 Start"
    MAIN_MENU = "💈 Main Menu"
    MINIMIZE_MENU = "➖ Minimize Menu"
    SAY_BYE = "🚪 Say 'Bye-Bye'"
    RETURN = "↪️ Return"


@dataclass
class SPECIAL_CHARACTERS:
    NO_ACTION_EMPTY_u200B = "\u200B"  # DO NOT CHANGE!!! ZERO-WIDTH EMPTY SYMBOL
    # Fot the future
    # FILL_IN_BLANK_SYMBOL = "\u0020"  # USING TO FILL IN BLANK SPACE WITH SPACES
