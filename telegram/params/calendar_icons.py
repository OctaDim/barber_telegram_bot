from dataclasses import dataclass


@dataclass
class CALENDAR_ICONS():
    NO_ICON: str = ""  # ATTENTION!!! DO NOT DELETE EMPTY ICONS. IT IS USED
    SELECTED: str = "✅"
    PREVIOUS_MONTH: str = "<<<"
    NEXT_MONTH: str = ">>>"
    WORKDAY: str = "🔵"
    WEEKEND: str = "🟣"
    TODAY: str = "🔸"
    CALENDAR: str = "📆"
    # CHECK_MARK: str = "📌"
