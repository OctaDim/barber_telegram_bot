from dataclasses import dataclass


@dataclass
class CALENDAR_ICONS:
    UNSELECTED_DAY: str = ""  # DON'T DELETE!!! IT IS USED!!!
    SELECTED: str = "✅"
    TO_PREVIOUS_MONTH: str = "<<<"
    TO_NEXT_MONTH: str = ">>>"
    WORKDAY: str = "🔵"
    WEEKEND: str = "🟣"
    TODAY_DATE: str = "🔸"
    CALENDAR: str = "📆"
