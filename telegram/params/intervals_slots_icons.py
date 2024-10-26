from dataclasses import dataclass


@dataclass
class SLOT_ICONS():
    NO_ICON: str = ""  # ATTENTION!!! DON'T DELETE EMPTY "NO_ICONS", IT IS USED!!!
    SLOT_POINT: str = "🔶"
    DATE_CALENDAR: str = "📆"
    TIME_SLOT_START_ICON: str = "➡️"
    TIME_SLOT_END_ICON: str = "⬅️"
    MOST_ADVISED_SLOT: str = "⭐️⭐️⭐️️"
    VERY_ADVISED_SLOT: str = "⭐️⭐️"
    ADVISED_SLOT: str = "⭐️"
    UNADVISED_SLOT: str = "❄️"
    VERY_UNADVISED_SLOT: str = "❄️❄️"
    UNSELECTED_SLOT = ""
    SELECTED_SLOT: str = "✅"

    # CHECK_MARK: str = "📌"
    # TEST: str = "🔆"
    # TEST: str = "❄️"
    # TEST: str = "*️⃣"
    # TEST: str = "🔷"
    # TEST: str = "✴️"
    # TEST: str = "❇️"
    # TEST: str = "✳️"
    # TEST: str = "▶️"
    # TEST: str = "➡️"
    # TEST: str = "✔️"
    # TEST: str = "☑️"
    # TEST: str = "🔘"
