from dataclasses import dataclass


@dataclass
class SLOT_ICONS():
    NO_ICON: str = ""  # DON'T DELETE!!! IT IS USED!!!
    SLOT_POINT: str = "🔶"
    DATE_CALENDAR: str = "📆"
    PREVIOUS_PAGE: str = "<<"
    NEXT_PAGE: str = ">>"
    TIME_SLOT_START_ICON: str = "➡️"
    TIME_SLOT_END_ICON: str = "⬅️"
    MAX_ADVISED_SLOT: str = "⭐️⭐️⭐️️⭐️⭐️"
    HIGHLY_ADVISED_SLOT: str = "⭐️⭐️⭐️⭐️"
    ADVISED_SLOT: str = "⭐️⭐️⭐️"
    STANDARD_SLOT: str = "⭐️⭐️"
    BASIC_SLOT: str = "⭐️"
    UNSELECTED_SLOT = ""
    SELECTED_SLOT_START_ICON: str = "✅"
    SELECTED_SLOT_END_ICON: str = "✅"
