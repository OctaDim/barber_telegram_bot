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
    NO_ACTION_EMPTY = "\u200B" # ATTENTION!!! DO NOT CHANGE!!! SPECIAL CHAR CODES AND SERVICE CHARACTERS
