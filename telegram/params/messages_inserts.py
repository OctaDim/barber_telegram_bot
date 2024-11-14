from dataclasses import dataclass


@dataclass
class MSG:
    NAME: str = "Name"
    MASTERS: str = "Masters"
    PRICE: str = "Price"
    DURATION: str = "Time duration"
    DESCRIPTION: str = "Description"

    SERVICES_TOTAL_COST: str = "💰 Total cost"
    SERVICES_TOTAL_DURATION: str = "🕑 Total time duration"
    SERVICES_TOTAL_COUNT: str = "✂️ Selected services count"

    CURRENCY_BRIEF: str = "byn"

    SERVICE_NAME: str = "Service"
    SERVICE_PRICE: str = "Price"
    SERVICE_DURATION: str = "Duration"
    SERVICE_DESCRIPTION: str = "Description"

    SOCIALS: str = "🌐 Social"
    PHONES: str = "📞 Phones"
    ADDRESSES: str = "📍 Address"

    SELECTED_DATE: str = "Selected date"
    SELECTED_INTERVAL_SLOT: str = "Selected time slot"

    SLOTS_RECOMMENDATIONS: str = "Recommendations"
    MAX_ADVISED_SLOTS: str = "Max recommended"
    HIGHLY_ADVISED_SLOTS: str = "Highly recommended"
    ADVISED_SLOT: str = "Recommended"
    STANDARD_SLOT: str = "Standard"
    BASIC_SLOTS: str = "Basic"
