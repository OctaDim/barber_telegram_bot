from dataclasses import dataclass


@dataclass
class COMMANDS_PARAMS:
    class START_CMD:
        TEXT: str = "start"
        DESCRIPTION: str = "🚀 СТАРТ"

    class MENU_CMD:
        TEXT: str = "menu"
        DESCRIPTION: str = "КАБИНЕТ КЛИЕНТА  👒🎩"


    class ADMIN_PANEL:
        TEXT: str = "admin"
        DESCRIPTION: str = "КАБИНЕТ АДМИНИСТРАТОРА  ⚙️"
