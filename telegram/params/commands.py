from dataclasses import dataclass


@dataclass
class COMMANDS_PARAMS:
    class START_CMD:
        TEXT: str = "start"
        DESCRIPTION: str = "🚀 Старт"

    class MENU_CMD:
        TEXT: str = "menu"
        DESCRIPTION: str = "💈 Главное Меню"


    class ADMIN_PANEL:
        TEXT: str = "admin"
        DESCRIPTION: str = "⚙️ Панель Админа"
