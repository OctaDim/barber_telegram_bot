from dataclasses import dataclass


@dataclass
class SELECT_SERVICES_ICONS():
    NO_ICON: str = ""  # ATTENTION!!! DO NOT DELETE EMPTY ICONS. IT IS USED
    UNSELECTED: str = "🟩"
    SELECTED: str = "✅"
    MARKER: str = "✂️"
