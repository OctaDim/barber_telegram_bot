from dataclasses import dataclass


@dataclass
class SELECT_SERVICES_ICONS():
    UNSELECTED: str = "🟩"
    SELECTED: str = "✅"
    NO_ICON: str = ""
    MARKER: str = "✂️"
