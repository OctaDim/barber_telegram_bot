from dataclasses import dataclass


@dataclass
class CALENDAR_ICONS():
    CHECK_MARK: str = "📌"
    NO_ICON: str = ""
    PREVIOUS_MONTH: str = "<<<"
    NEXT_MONTH: str = ">>>"
    WORKDAY: str = "🔵"
    WEEKEND: str = "🟣"
    TODAY: str = "🔸"
