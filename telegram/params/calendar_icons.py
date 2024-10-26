from dataclasses import dataclass


@dataclass
class CALENDAR_ICONS():
    UNSELECTED_DAY: str = ""  # DON'T DELETE!!! IT IS USED!!!
    SELECTED: str = "✅"
    PREVIOUS_MONTH: str = "<<<"
    NEXT_MONTH: str = ">>>"
    WORKDAY: str = "🔵"
    WEEKEND: str = "🟣"
    TODAY_DATE: str = "🔸"
    CALENDAR: str = "📆"
