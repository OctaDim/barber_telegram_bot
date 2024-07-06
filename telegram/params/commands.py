from dataclasses import dataclass


@dataclass
class COMMANDS_PARAMS:
    class START_CMD:
        TEXT: str = "start"
        DESCRIPTION: str = "🚀 Start"

    class MENU_CMD:
        TEXT: str = "menu"
        DESCRIPTION: str = "💈 Main Menu"


    class ADMIN_PANEL:
        TEXT: str = "admin"
        DESCRIPTION: str = "⚙️ Admin Panel"
