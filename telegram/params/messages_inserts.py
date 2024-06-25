from dataclasses import dataclass


@dataclass
class MSG:
    NAME: str = "Name"
    PRICE: str = "Price"
    DURATION: str = "Time duration"
    DESCRIPTION: str = "Description"

    SERVICES_TOTAL_COST: str = "Total cost💰:"
    SERVICES_TOTAL_DURATION: str = "Total time duration⌚️:"
    SERVICES_TOTAL_COUNT: str = "Selected service(s)✂️ (count):"

    CURRENCY_BRIEF: str = "byn"

    SERVICE_NAME: str = "Service name"
    SERVICE_PRICE: str = "Price"
    SERVICE_DURATION: str = "Duration"
    SERVICE_DESCRIPTION: str = "Description"
